output "ec2_public_ip" {
  description = "EC2 Public IP"
  value       = aws_instance.app.public_ip
}

output "rds_endpoint" {
  description = "RDS Endpoint"
  value       = aws_db_instance.postgres.endpoint
}