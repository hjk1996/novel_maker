
output "subnet_id" {
  value = module.vpc.public_subnets[0]
}

output "sg_id" {
  value = aws_security_group.app_sg.id
}