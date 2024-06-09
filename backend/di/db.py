import boto3



dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
book_table = dynamodb.Table("novel-maker-book-table")
chapter_table = dynamodb.Table("novel-maker-chapter-table")
s3 = boto3.resource("s3", region_name="ap-northeast-2")
book_cover_bucket = s3.Bucket("novel-maker-book-cover-bucket")


def get_book_table():
    return book_table

def get_chapter_table():
    return chapter_table


def get_book_cover_bucket():
    return book_cover_bucket