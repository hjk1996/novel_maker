
output "cognito_domain" {
  value = module.cognito_module.cognito_domain
}

output "user_pool_id" {
  value = module.cognito_module.user_pool_id
}

output "app_client_id" {
  value = module.cognito_module.app_client_id
}