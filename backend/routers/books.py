import uuid
from datetime import datetime, timezone


from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from chat_agents import NextStoryAgent, ChoicesAgent
from models import Book
from db import get_table


router = APIRouter()
next_stroy_agent = NextStoryAgent()
choices_agent = ChoicesAgent()


class BookCreate(BaseModel):
    title: str
    genres: list[str]


@router.post(
    "/users/{user_id}/books/",
    response_model=Book,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def create_book(user_id: int, book: BookCreate):
    table = get_table("Books")
    book_id = uuid.uuid4()
    timestamp = int(datetime.now(timezone.utc).timestamp())
    new_book = {
        "id": book_id,
        "user_id": user_id,
        "title": book.title,
        "genres": book.genres,
        "created_at": timestamp,
    }
    response = table.put_item(
        Item=new_book,
    )
    return new_book


@router.get("/users/{user_id}/books/")
async def get_user_books(user_id: str):
    table = get_table("Books")
    response = table.scan(
        FilterExpression=["user_id = :user_id"],
        ExpressionAttributeValues={
            ":user_id": user_id,
        },
    )
    items = response.get("Items", [])
    return items


@router.get("/users/{user_id}/books/{book_id}", status_code=status.HTTP_200_OK)
def get_book(user_id: str, book_id: str):
    table = get_table("Books")
    response = table.get_item(Key={"id": book_id, "user_id": user_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Book not found")
    return item


@router.delete("/users/{user_id}/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(user_id: int, book_id: int): ...


@router.post("/users/{user_id}/books/{book_id}/choices")
def create_choices(user_id: int, book_id: int): ...


@router.post("/users/{user_id}/books/{book_id}/next-story")
def create_next_story(user_id: int, book_id: int): ...
