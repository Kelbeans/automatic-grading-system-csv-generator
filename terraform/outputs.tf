output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.sf10_server.id
}

output "instance_public_ip" {
  description = "Public IP address (Elastic IP)"
  value       = aws_eip.sf10_eip.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name"
  value       = aws_instance.sf10_server.public_dns
}

output "app_url" {
  description = "Application URL"
  value       = "http://${aws_eip.sf10_eip.public_ip}"
}

output "ssh_command" {
  description = "SSH command to connect to the server"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_eip.sf10_eip.public_ip}"
}
