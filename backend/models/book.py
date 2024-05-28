from pydantic import BaseModel, Field


class Book(BaseModel):

    id: str
    user_id: str
    title: str
    cover_url: str | None = None
    genres: list[str]
    created_at: int
