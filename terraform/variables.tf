variable "aws_region" {
  description = "AWS Region"
  default     = "ap-southeast-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public Subnet CIDR"
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "Private Subnet CIDR"
  default     = "10.0.2.0/24"
}

variable "app_name" {
  description = "Application name"
  default     = "taskmanager"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.micro"
}

variable "db_password" {
  description = "Database password"
  default     = "postgres123"
}