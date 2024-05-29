import uuid
from datetime import datetime, timezone


from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from chat_agents import NextStoryAgent, ChoicesAgent
from models import Book, Chapter, Choices
from db import get_book_table


router = APIRouter()
next_stroy_agent = NextStoryAgent()
choices_agent = ChoicesAgent()
book_table = get_book_table()


class CreateBookBody(BaseModel):
    title: str
    genres: list[str]


@router.post(
    "/users/{user_id}/books/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(user_id: str, body: CreateBookBody):
    book_id = str(uuid.uuid4())
    timestamp = int(datetime.now(timezone.utc).timestamp())
    new_book = {
        "id": book_id,
        "user_id": user_id,
        "title": body.title,
        "genres": body.genres,
        "created_at": timestamp,
        "chapters": [],
    }
    response = book_table.put_item(
        Item=new_book, ConditionExpression="attribute_not_exists(id)"
    )
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to create book item")

    return new_book


class UserBookListItemSchema(BaseModel):
    id: str
    user_id: str
    title: str
    cover_url: str | None = None
    genres: list[str]
    created_at: int


@router.get(
    "/users/{user_id}/books/",
    response_model=list[UserBookListItemSchema],
    status_code=status.HTTP_200_OK,
)
async def get_user_book_list(user_id: str):
    response = book_table.scan(
        FilterExpression="user_id = :user_id",
        ExpressionAttributeValues={
            ":user_id": user_id,
        },
        ProjectionExpression="id, user_id, title, cover_url, genres, created_at",
    )
    items = response.get("Items", [])
    return items


@router.get(
    "/users/{user_id}/books/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
)
async def get_book(user_id: str, book_id: str):
    response = book_table.get_item(Key={"id": book_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Book not found")
    return item


class UpdateBookBody(BaseModel):
    title: str | None = None
    genres: list[str] = None
    book_language: str | None = None
    chapters: list[Chapter] | None = None


@router.patch(
    "/users/{user_id}/books/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
)
async def update_book(user_id: str, book_id: str, body: UpdateBookBody):
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

    if not update_expressions:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_expression = "SET " + ", ".join(update_expressions)

    response = book_table.update_item(
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
def delete_book(user_id: str, book_id: str):
    response = book_table.delete_item(Key={"id": book_id})
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to delete book item")
    return None


@router.post(
    "/users/{user_id}/books/{book_id}/choices",
    response_model=Choices,
    status_code=status.HTTP_200_OK,
)
async def generate_choices(user_id: str, book_id: str, body: Book):
    story = body.get_story()
    choices = choices_agent(language=body.book_language, previous_story=story)
    return choices


class NextStoryBody(BaseModel):
    book: Book
    choice: str


@router.post(
    "/users/{user_id}/books/{book_id}/next-story",
    response_model=Book,
    status_code=status.HTTP_200_OK,
)
async def generate_next_story(user_id: str, book_id: str, body: NextStoryBody):
    story = body.book.get_story()
    next_story = next_stroy_agent(
        genres=body.book.genres,
        language=body.book.book_language,
        previous_story=story,
        choice=body.choice,
    )
    new_book = body.book.model_copy()
    new_book.chapters[-1].content += " " + next_story.content

    response = book_table.update_item(
        Key={"id": book_id},
        UpdateExpression="SET chapters = :chapters",
        ExpressionAttributeValues={
            ":chapters": [chapter.model_dump() for chapter in new_book.chapters]
        },
        ReturnValues="ALL_NEW",
    )

    updated_book = response.get("Attributes")
    if not updated_book:
        raise HTTPException(status_code=404, detail="Failed to update chapter")
    return updated_book
