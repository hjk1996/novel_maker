data "aws_region" "current" {

}

resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-cluster"
}

resource "aws_cloudwatch_log_group" "app_log_group" {
  name = "${var.app_name}-log-group"
}

resource "aws_ecs_task_definition" "novel_maker" {
  family                   = "novel-maker"
  cpu                      = 256
  memory                   = 512
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  execution_role_arn = var.app_execution_role_arn
  task_role_arn      = var.app_role_arn


  container_definitions = jsonencode([
    {
      name      = "novel-maker"
      image     = "hjk1996/novel-maker:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "TCP"
        }
      ]
      environment = [
        for k, v in var.app_environment_variables : {
            name = k 
            value = v
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app_log_group.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}


resource "aws_ecs_service" "novel_maker" {
  name            = "${var.app_name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.novel_maker.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [var.subnet_id]
    security_groups  = [var.sg_id]
    assign_public_ip = true
  }
}