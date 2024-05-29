import boto3

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
book_table = dynamodb.Table("novel-maker-book-table")
chapter_table = dynamodb.Table("novel-maker-chapter-table")

def get_book_table():
    return book_table

def get_chapter_table():
    return chapter_table  

