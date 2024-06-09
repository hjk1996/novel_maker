variable "app_name" {
  type = string
}

variable "app_role_arn" {
  type = string
}

variable "app_execution_role_arn" {
  type = string
}

variable "app_environment_variables" {
  type = map(string)
}



variable "subnet_id" {
  type = string
}

variable "sg_id" {
  type = string
}