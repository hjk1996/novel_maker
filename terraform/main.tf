module "dynamodb_module" {
  source   = "./modules/dynamodb"
  app_name = var.app_name
}

module "cognito_module" {
  source   = "./modules/cognito"
  app_name = var.app_name

}

module "s3_module" {
  source   = "./modules/s3"
  app_name = var.app_name

}

module "iam_module" {
  source     = "./modules/iam"
  app_name   = var.app_name
  openai_api_key_parameter_name = module.ssm_module.openai_api_key_parameter_name
  depends_on = [module.cognito_module, module.ssm_module]
}

module "vpc_module" {
  source   = "./modules/vpc"
  app_name = var.app_name

}

data "aws_region" "current" {
  
}

module "ecs_module" {
  source       = "./modules/ecs"
  app_name     = var.app_name
  app_role_arn = module.iam_module.app_role_arn
  depends_on   = [module.iam_module]
  subnet_id    = module.vpc_module.subnet_id
  sg_id        = module.vpc_module.sg_id
  app_execution_role_arn = module.iam_module.app_task_execution_role_arn
  app_environment_variables = {
    MODEL = "gpt-4o"
    COGNITO_USER_POOL_ID = module.cognito_module.user_pool_id
    COGNITO_APP_CLIENT_ID = module.cognito_module.app_client_id
    REGION = data.aws_region.current.name
  }

}

module "ssm_module" {
  source = "./modules/ssm"
  app_name = var.app_name
  app_openai_api_key = var.app_openai_api_key
  
}