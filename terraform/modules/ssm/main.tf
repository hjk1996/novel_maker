resource "aws_ssm_parameter" "app_openai_api_key" {
  name  = "${var.app_name}-openai-api-key"
  type  = "String"
  value = var.app_openai_api_key
}
