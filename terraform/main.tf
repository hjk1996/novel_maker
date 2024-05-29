module "dynamodb_module" {
    source = "./modules/dynamodb"
}

module "cognito_module" {
  source = "./modules/cognito"
}

