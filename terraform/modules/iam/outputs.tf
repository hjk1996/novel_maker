

output "app_role_arn" {
  value = aws_iam_role.app_role.arn
}

output "app_task_execution_role_arn" {
  value = aws_iam_role.app_task_execution_role.arn
}