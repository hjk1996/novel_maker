

resource "aws_dynamodb_table" "book_table" {
    name = "novel-maker-book-table"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "id"

    attribute {
      name = "id"
      type = "S"
    }



}







