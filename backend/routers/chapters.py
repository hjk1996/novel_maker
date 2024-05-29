from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from models import Chapter
from db import get_chapter_table


router = APIRouter()
chapter_table = get_chapter_table()


class ChapterCreate(BaseModel):
    chapter_name: str


@router.post(
    "/users/{user_id}/books/{book_id}/chapters/{chapter_number}",
    response_model=Chapter,
    status_code=status.HTTP_201_CREATED,
)
def create_chapter(
    user_id: str, book_id: str, chapter_number: int, body: ChapterCreate
):
    timestamp = int(datetime.now(timezone.utc).timestamp())
    chapter = {
        "book_id": book_id,
        "chapter_number": chapter_number,
        "created_at": timestamp,
        "chapter_name": body.chapter_name,
        "contents": [],
    }
    response = chapter_table.put_item(
        Item=chapter, ConditionExpression="attribute_not_exists(chapter_number)"
    )
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to create chapter")
    return chapter


class RenameChapterBody(BaseModel):
    chapter_name: str


class UpdateChapterBody(BaseModel):
    chapter_name: str | None = None
    contents: list[str] | None = None


@router.patch(
    "/users/{user_id}/books/{book_id}/chapters/{chapter_number}",
    response_model=Chapter,  # Assuming Chapter is a dict, adjust if needed
    status_code=status.HTTP_200_OK,
)
def update_chapter(
    user_id: str, book_id: str, chapter_number: int, body: UpdateChapterBody
):
    update_expressions = []
    expression_attribute_values = {}

    if body.chapter_name is not None:
        update_expressions.append("chapter_name = :chapter_name")
        expression_attribute_values[":chapter_name"] = body.chapter_name

    if body.contents is not None:
        update_expressions.append("contents = :contents")
        expression_attribute_values[":contents"] = body.contents

    if not update_expressions:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_expression = "SET " + ", ".join(update_expressions)

    response = chapter_table.update_item(
        Key={"book_id": book_id, "chapter_number": chapter_number},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )
    updated_chapter = response.get("Attributes")
    if not updated_chapter:
        raise HTTPException(status_code=404, detail="Failed to update chapter")

    return updated_chapter


@router.get(
    "/users/{user_id}/books/{book_id}/chapters",
    response_model=list[Chapter],
    status_code=status.HTTP_200_OK,
)
def get_chapters(user_id: str, book_id: str):
    response = chapter_table.scan(
        FilterExpression="book_id = :book_id",
        ExpressionAttributeValues={":book_id": book_id},
    )
    items = response.get("Items", [])
    return items


@router.delete(
    "/users/{user_id}/books/{book_id}/chapters/{chapter_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_chapter(user_id: str, book_id: str, chapter_number: int):
    response = chapter_table.delete_item(
        Key={"book_id": book_id, "chapter_number": chapter_number}
    )
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to delete chapter")
    return None
