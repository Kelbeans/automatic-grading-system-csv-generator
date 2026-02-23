terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

# Security Group
resource "aws_security_group" "sf10_sg" {
  name        = "sf10-grade-automation-sg"
  description = "Security group for SF10 Grade Automation"

  # SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }

  # HTTP access
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access"
  }

  # HTTPS access
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS access"
  }

  # Flask app port (for direct access during setup)
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Flask app port"
  }

  # Outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  tags = {
    Name = "sf10-grade-automation-sg"
  }
}

# EC2 Key Pair
resource "aws_key_pair" "sf10_key" {
  key_name   = "sf10-grade-automation-key"
  public_key = file(var.ssh_public_key_path)
}

# EC2 Instance
resource "aws_instance" "sf10_server" {
  ami           = var.ami_id
  instance_type = var.instance_type

  key_name               = aws_key_pair.sf10_key.key_name
  vpc_security_group_ids = [aws_security_group.sf10_sg.id]

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  user_data = templatefile("${path.module}/user_data.sh", {
    github_repo = var.github_repo
  })

  tags = {
    Name = "sf10-grade-automation-server"
  }
}

# Elastic IP
resource "aws_eip" "sf10_eip" {
  instance = aws_instance.sf10_server.id
  domain   = "vpc"

  tags = {
    Name = "sf10-grade-automation-eip"
  }
}
