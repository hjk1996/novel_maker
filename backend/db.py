import boto3

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")


def get_table(table_name: str):
    return dynamodb.Table(table_name)
