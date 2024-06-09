output "cognito_domain" {
  value = aws_cognito_user_pool_domain.user_pool_domain.domain
}

output "user_pool_id" {
  value = aws_cognito_user_pool.user_pool.id
}

output "app_client_id" {
  value = aws_cognito_user_pool_client.user_pool_client.id
}