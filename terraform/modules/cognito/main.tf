resource "aws_cognito_user_pool" "user_pool" {
  name = "novel-maker-user-pool"

  # 비밀번호 정책
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  # 이메일 
  schema {
    name     = "email"
    required = true
    mutable  = false

    attribute_data_type      = "String"
    developer_only_attribute = false
    string_attribute_constraints {
      min_length = 5
      max_length = 50
    }
  }


  admin_create_user_config {
    allow_admin_create_user_only = false
  }

  # 이거 설정해야 이메일 회원가입할 때 자동으로 인증 메일 보내줌
  auto_verified_attributes = ["email"]

  # 이메일 인증 템플릿
  verification_message_template {
    email_message        = "Your verification code is {####}"
    email_subject        = "Verify your email for our app"
    default_email_option = "CONFIRM_WITH_CODE"
  }
}

resource "aws_cognito_user_pool_domain" "user_pool_domain" {
  domain       = "novel-maker-user-pool-domain"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}


# 파라미터 스토어에 저장된 구글 클라이언트 아이디와 시크릿
data "aws_ssm_parameter" "google_client_id" {
  name = "novel-maker-google-client-id"
}

data "aws_ssm_parameter" "google_client_secret" {
  name = "novel-maker-google-client-secret"
}


# 구글 oidc 연결
resource "aws_cognito_identity_provider" "google" {
  user_pool_id  = aws_cognito_user_pool.user_pool.id
  provider_name = "Google"
  provider_type = "Google"
  provider_details = {
    client_id        = data.aws_ssm_parameter.google_client_id.value
    client_secret    = data.aws_ssm_parameter.google_client_secret.value
    authorize_scopes = "openid profile email"
  }
}


resource "aws_cognito_user_pool_client" "user_pool_client" {
  name         = "novel-maker-user-pool-client"
  user_pool_id = aws_cognito_user_pool.user_pool.id

  explicit_auth_flows = [
    "ALLOW_ADMIN_USER_PASSWORD_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_CUSTOM_AUTH",
    "ALLOW_USER_SRP_AUTH",
  ]

  supported_identity_providers = ["Google"]

  allowed_oauth_flows  = ["code", "implicit"]
  allowed_oauth_scopes = ["phone", "email", "openid", "profile", "aws.cognito.signin.user.admin"]


  callback_urls = ["http://localhost:3000/auth/callback"]
  logout_urls   = ["http://localhost:3000/auth/logout"]

  prevent_user_existence_errors = "ENABLED"

  token_validity_units {
    access_token  = "hours"
    id_token      = "hours"
    refresh_token = "days"
  }

  access_token_validity  = 1
  id_token_validity      = 1
  refresh_token_validity = 30
}


