# AWS Deployment with Terraform + CI/CD

This directory contains Terraform configuration to deploy SF10 Grade Automation to AWS with automatic CI/CD via GitHub Actions.

## What This Does

- **Provisions AWS infrastructure** (EC2, Security Groups, Elastic IP)
- **Installs and configures** the app automatically
- **Sets up Nginx** as reverse proxy
- **Creates systemd service** for auto-restart
- **Enables CI/CD** - deploys automatically on git push to main

## Prerequisites

### 1. AWS Account
- Sign up at https://aws.amazon.com
- **Free tier eligible** (t2.micro instance)
- Free for 12 months, then ~$5-10/month

### 2. Install Terraform
```bash
# macOS
brew install terraform

# Windows (with Chocolatey)
choco install terraform

# Or download from: https://www.terraform.io/downloads
```

### 3. Install AWS CLI
```bash
# macOS
brew install awscli

# Windows
# Download from: https://aws.amazon.com/cli/
```

### 4. SSH Key Pair
Generate if you don't have one:
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

## Step 1: Configure AWS Credentials

### Create IAM User
1. Go to AWS Console → IAM → Users
2. Click **"Add users"**
3. Username: `terraform-user`
4. Access type: **Programmatic access**
5. Permissions: Attach **AdministratorAccess** (or EC2FullAccess minimum)
6. Save **Access Key ID** and **Secret Access Key**

### Configure AWS CLI
```bash
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: ap-southeast-1 (Singapore)
# - Output format: json
```

## Step 2: Deploy with Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Preview what will be created
terraform plan

# Deploy to AWS (takes ~5 minutes)
terraform apply
# Type 'yes' when prompted

# Save the outputs (IP address, SSH command, etc.)
```

### Terraform will create:
- ✅ EC2 t2.micro instance (Ubuntu 22.04)
- ✅ Security Group (allows HTTP, HTTPS, SSH)
- ✅ Elastic IP (static IP address)
- ✅ SSH key pair
- ✅ Full app installation and configuration

### After deployment, you'll see:
```
Outputs:

app_url = "http://13.229.XXX.XXX"
instance_public_ip = "13.229.XXX.XXX"
ssh_command = "ssh -i ~/.ssh/id_rsa ubuntu@13.229.XXX.XXX"
```

🎉 **Your app is now live!** Visit the `app_url` in your browser.

## Step 3: Set Up CI/CD (Auto-Deploy on Git Push)

### Add GitHub Secrets
Go to your repo → Settings → Secrets and variables → Actions → New repository secret

Add these 3 secrets:

#### 1. AWS_ACCESS_KEY_ID
- Value: Your AWS Access Key ID from Step 1

#### 2. AWS_SECRET_ACCESS_KEY
- Value: Your AWS Secret Access Key from Step 1

#### 3. EC2_SSH_PRIVATE_KEY
- Get your private key:
  ```bash
  cat ~/.ssh/id_rsa
  ```
- Copy the **entire content** including:
  ```
  -----BEGIN OPENSSH PRIVATE KEY-----
  ...
  -----END OPENSSH PRIVATE KEY-----
  ```

#### 4. EC2_HOST
- Value: The **Elastic IP** from Terraform output (e.g., `13.229.XXX.XXX`)

### Test CI/CD
```bash
# Make a change
echo "# Test" >> README.md

# Commit and push
git add .
git commit -m "test: Trigger CI/CD deployment"
git push origin main
```

Go to GitHub → Actions tab → Watch the deployment!

## How CI/CD Works

```
Push to main → GitHub Actions → Deploy to EC2 → App restarts
```

Every time you push to `main` branch:
1. GitHub Actions triggers
2. Connects to your EC2 instance via SSH
3. Pulls latest code from GitHub
4. Installs dependencies
5. Restarts the Flask app
6. Deployment complete! (~30 seconds)

## Customization

### Change AWS Region
Edit `terraform/variables.tf`:
```hcl
variable "aws_region" {
  default = "us-east-1"  # Change to your preferred region
}

variable "ami_id" {
  default = "ami-0c7217cdde317cfec"  # Update AMI for the region
}
```

### Change Instance Type
Edit `terraform/variables.tf`:
```hcl
variable "instance_type" {
  default = "t2.small"  # More RAM (~$15/month)
}
```

## SSH Access

Connect to your server:
```bash
ssh -i ~/.ssh/id_rsa ubuntu@YOUR_ELASTIC_IP
```

### Useful Commands
```bash
# Check app status
sudo systemctl status sf10

# View app logs
sudo journalctl -u sf10 -f

# Restart app
sudo systemctl restart sf10

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Manual deployment
sudo -u sf10app /home/sf10app/deploy.sh
```

## Updating the App

### Option 1: Automatic (Recommended)
Just push to GitHub:
```bash
git add .
git commit -m "feat: New feature"
git push origin main
```
CI/CD handles the rest!

### Option 2: Manual SSH
```bash
ssh -i ~/.ssh/id_rsa ubuntu@YOUR_IP
sudo -u sf10app /home/sf10app/deploy.sh
```

## Costs

### Free Tier (First 12 Months)
- ✅ t2.micro instance: **750 hours/month FREE**
- ✅ 30 GB storage: **FREE**
- ✅ 15 GB bandwidth: **FREE**
- ✅ Elastic IP (while attached): **FREE**

### After Free Tier
- 💵 t2.micro: ~$8/month (always on)
- 💵 Storage: ~$3/month
- 💵 Bandwidth: ~$1-2/month
- **Total: ~$10-12/month**

### Cost Optimization
Stop instance when not in use:
```bash
# Stop (preserves data, no compute charges)
aws ec2 stop-instances --instance-ids <INSTANCE_ID>

# Start
aws ec2 start-instances --instance-ids <INSTANCE_ID>
```

## Troubleshooting

### Deployment Failed
Check GitHub Actions logs for errors.

### Can't Access App
1. Check security group allows HTTP (port 80)
2. Verify Elastic IP is attached
3. SSH in and check: `sudo systemctl status sf10`

### App Not Starting
```bash
# SSH into server
ssh -i ~/.ssh/id_rsa ubuntu@YOUR_IP

# Check logs
sudo journalctl -u sf10 -n 50

# Restart
sudo systemctl restart sf10
```

### Out of Memory
Upgrade to t2.small:
```bash
cd terraform
# Edit variables.tf, change instance_type to "t2.small"
terraform apply
```

## Destroy Infrastructure

When done, remove everything:
```bash
cd terraform
terraform destroy
# Type 'yes' to confirm
```

This removes all AWS resources and stops charges.

## Support

- Terraform docs: https://www.terraform.io/docs
- AWS Free Tier: https://aws.amazon.com/free
- GitHub Actions: https://docs.github.com/actions

---

**Author**: Kelvin A. Malabanan
**Repository**: https://github.com/Kelbeans/automatic-grading-system-csv-generator
