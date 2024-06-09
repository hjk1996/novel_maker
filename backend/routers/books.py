import io
import uuid
from datetime import datetime, timezone


from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
from pydantic import BaseModel


from di.auth import get_current_user
from di.db import get_book_table, get_book_cover_bucket
from models import TokenPayload
from models import Book, Chapter


router = APIRouter()


class CreateBookBody(BaseModel):
    title: str
    description: str
    genres: list[str]


@router.post(
    "/users/{user_id}/new-book/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    user_id: str,
    body: CreateBookBody,
    table=Depends(get_book_table),
    current_user: TokenPayload = Depends(get_current_user),
):

    if user_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create books for this user",
        )

    book_id = str(uuid.uuid4())
    timestamp = int(datetime.now(timezone.utc).timestamp())
    new_book = {
        "id": book_id,
        "user_id": user_id,
        "title": body.title,
        "description": body.description,
        "genres": body.genres,
        "created_at": timestamp,
        "chapters": [],
    }
    response = table.put_item(
        Item=new_book, ConditionExpression="attribute_not_exists(id)"
    )
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to create book item")

    return new_book


@router.get(
    "/users/{user_id}/books/",
    response_model=list[Book],
    status_code=status.HTTP_200_OK,
)
async def get_user_book_list(
    user_id: str,
    table=Depends(get_book_table),
    current_user: TokenPayload = Depends(get_current_user),
):
    if user_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's books",
        )

    response = table.scan(
        FilterExpression="user_id = :user_id",
        ExpressionAttributeValues={
            ":user_id": user_id,
        },
    )
    items = response.get("Items", [])
    return items


@router.get(
    "/users/{user_id}/books/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
)
async def get_book(
    user_id: str,
    book_id: str,
    table=Depends(get_book_table),
    current_user: TokenPayload = Depends(get_current_user),
):
    if user_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's books",
        )
    response = table.get_item(Key={"id": book_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Book not found")
    return item


class UpdateBookBody(BaseModel):
    title: str | None = None
    genres: list[str] = None
    book_language: str | None = None
    chapters: list[Chapter] | None = None
    cover_url: str | None = None


@router.patch(
    "/users/{user_id}/books/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
)
async def update_book(
    user_id: str,
    book_id: str,
    body: UpdateBookBody,
    table=Depends(get_book_table),
    current_user: TokenPayload = Depends(get_current_user),
):
    if user_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's books",
        )

    update_expressions = []
    expression_attribute_values = {}

    if body.title is not None:
        update_expressions.append("title = :title")
        expression_attribute_values[":title"] = body.title

    if body.book_language is not None:
        update_expressions.append("book_language = :book_language")
        expression_attribute_values[":book_language"] = body.book_language

    if body.genres is not None:
        update_expressions.append("genres = :genres")
        expression_attribute_values[":genres"] = body.genres

    if body.chapters is not None:
        update_expressions.append("chapters = :chapters")
        expression_attribute_values[":chapters"] = [
            chapter.model_dump() for chapter in body.chapters
        ]

    if body.cover_url is not None:
        update_expressions.append("cover_url = :cover_url")
        expression_attribute_values[":cover_url"] = body.cover_url

    if not update_expressions:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_expression = "SET " + ", ".join(update_expressions)

    response = table.update_item(
        Key={"id": book_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )
    updated_book = response.get("Attributes")
    if not updated_book:
        raise HTTPException(status_code=404, detail="Failed to update chapter")

    return updated_book


@router.delete(
    "/users/{user_id}/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_book(
    user_id: str,
    book_id: str,
    table=Depends(get_book_table),
    current_user: TokenPayload = Depends(get_current_user),
):
    if user_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's books",
        )

    response = table.delete_item(Key={"id": book_id})
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to delete book item")
    return None


@router.post(
    "/users/{user_id}/books/{book_id}/book-cover",
    status_code=status.HTTP_201_CREATED,
)
async def save_book_cover(
    user_id: str,
    book_id: str,
    file: UploadFile = File(),
    table=Depends(get_book_table),
    bucket=Depends(get_book_cover_bucket),
    current_user: TokenPayload = Depends(get_current_user),
):
    if user_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's books",
        )

    bytes_data = await file.read()

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{user_id}/{book_id}/book_cover.{file_extension}"

    # S3에 파일 업로드
    bucket.put_object(
        Key=unique_filename, Body=bytes_data, ContentType=file.content_type
    )

    # 업로드된 파일의 URL 생성
    file_url = (
        f"https://{bucket.name}.s3.ap-northeast-2.amazonaws.com/{unique_filename}"
    )

    table.update_item(
        Key={"id": book_id},
        UpdateExpression="SET cover_url = :v",
        ExpressionAttributeValues={":v": file_url},
        ReturnValues="ALL_NEW",
    )
    
    

    return {"file_url": file_url}
