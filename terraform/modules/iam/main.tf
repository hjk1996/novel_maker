


data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_iam_role" "app_role" {
  name = "${var.app_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}


data "aws_cognito_user_pools" "app_user_pool" {
  name = "${var.app_name}-user-pool"
}


resource "aws_iam_policy" "app_iam_role_policy" {
  name = "${var.app_name}-role-policy"
  policy = jsonencode(
    {
      Version = "2012-10-17",
      Statement = [
        {

          Effect = "Allow",
          Action = [
            "dynamodb:BatchGetItem",
            "dynamodb:BatchWriteItem",
            "dynamodb:DeleteItem",
            "dynamodb:GetItem",
            "dynamodb:PutItem",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:UpdateItem"
          ],
          Resource = "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${var.app_name}-book-table"
        },
        {
          Effect = "Allow",
          Action = [
            "s3:PutObject",
            "s3:GetObject",
            "s3:DeleteObject",
            "s3:ListBucket"
          ],
          Resource = [
            "arn:aws:s3:::${var.app_name}-book-cover-bucket",
            "arn:aws:s3:::${var.app_name}-book-cover-bucket/*"
          ]
        },
        {
          Effect = "Allow",
          Action = [
            "cognito-idp:SignUp",
            "cognito-idp:ConfirmSignUp",
            "cognito-idp:InitiateAuth",
            "cognito-idp:AdminInitiateAuth"
          ],
          Resource = [
            "arn:aws:cognito-idp:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:userpool/*"
          ]
        },
          {
        Effect = "Allow",
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParameterHistory",
          "ssm:GetParametersByPath"
        ],
        Resource = [
          "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/${var.openai_api_key_parameter_name}",
        ]
      }

      ]

    },


  )

}

resource "aws_iam_role_policy_attachment" "attachment_1" {
  role       = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.app_iam_role_policy.arn
}

resource "aws_iam_role" "app_task_execution_role" {
  name = "${var.app_name}-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.app_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "cloudwatch_logs_policy" {
  role       = aws_iam_role.app_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}