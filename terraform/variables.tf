variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "ap-southeast-1" # Singapore (closest to Philippines)
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro" # Free tier eligible
}

variable "ami_id" {
  description = "Ubuntu 22.04 LTS AMI ID for the region"
  type        = string
  # Default: Ubuntu 22.04 LTS in ap-southeast-1 (Singapore)
  default = "ami-0497a974f8d5dcef8"
  # Note: AMI IDs vary by region. Update if using different region:
  # us-east-1: ami-0c7217cdde317cfec
  # us-west-2: ami-0efcece6bed30fd98
  # eu-west-1: ami-0905a3c97561e0b69
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key file"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "github_repo" {
  description = "GitHub repository URL"
  type        = string
  default     = "https://github.com/Kelbeans/automatic-grading-system-csv-generator.git"
}
