output "cognito_domain" {
  value = aws_cognito_user_pool_domain.user_pool_domain.domain
}