data "aws_region" "current" {

}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.app_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${data.aws_region.current.name}a"]
  private_subnets = ["10.0.1.0/24"]
  public_subnets  = ["10.0.101.0/24"]



  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

resource "aws_security_group" "app_sg" {
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}