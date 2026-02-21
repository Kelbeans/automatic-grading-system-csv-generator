#!/bin/bash
set -e

# Log everything
exec > >(tee /var/log/user-data.log)
exec 2>&1

echo "========================================="
echo "SF10 Grade Automation - Server Setup"
echo "========================================="

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Python and dependencies
echo "Installing Python 3.11..."
apt-get install -y python3.11 python3.11-venv python3-pip nginx git

# Create app user
echo "Creating app user..."
useradd -m -s /bin/bash sf10app || true

# Clone repository
echo "Cloning repository..."
cd /home/sf10app
rm -rf automatic-grading-system
sudo -u sf10app git clone ${github_repo} automatic-grading-system
cd automatic-grading-system

# Create virtual environment
echo "Setting up Python virtual environment..."
sudo -u sf10app python3.11 -m venv venv
sudo -u sf10app /home/sf10app/automatic-grading-system/venv/bin/pip install --upgrade pip
sudo -u sf10app /home/sf10app/automatic-grading-system/venv/bin/pip install -r requirements.txt
sudo -u sf10app /home/sf10app/automatic-grading-system/venv/bin/pip install gunicorn

# Create systemd service
echo "Creating systemd service..."
cat > /etc/systemd/system/sf10.service <<'EOF'
[Unit]
Description=SF10 Grade Automation Flask App
After=network.target

[Service]
User=sf10app
Group=sf10app
WorkingDirectory=/home/sf10app/automatic-grading-system
Environment="PATH=/home/sf10app/automatic-grading-system/venv/bin"
ExecStart=/home/sf10app/automatic-grading-system/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8080 sf10_web_app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "Configuring Nginx..."
cat > /etc/nginx/sites-available/sf10 <<'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
EOF

ln -sf /etc/nginx/sites-available/sf10 /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Start services
echo "Starting services..."
systemctl daemon-reload
systemctl enable sf10
systemctl start sf10
systemctl restart nginx

# Create deployment script for CI/CD
echo "Creating deployment script..."
cat > /home/sf10app/deploy.sh <<'EOF'
#!/bin/bash
set -e

echo "Deploying SF10 Grade Automation..."

cd /home/sf10app/automatic-grading-system

# Pull latest code
git fetch origin
git reset --hard origin/main

# Install/update dependencies
/home/sf10app/automatic-grading-system/venv/bin/pip install -r requirements.txt

# Restart service
sudo systemctl restart sf10

echo "Deployment complete!"
EOF

chmod +x /home/sf10app/deploy.sh
chown sf10app:sf10app /home/sf10app/deploy.sh

# Allow sf10app user to restart service without password
echo "sf10app ALL=(ALL) NOPASSWD: /bin/systemctl restart sf10" >> /etc/sudoers.d/sf10app

echo "========================================="
echo "Setup Complete!"
echo "App should be accessible at http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "========================================="
