

resource "aws_dynamodb_table" "book_table" {
  name         = "${var.app_name}-book-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }



}







