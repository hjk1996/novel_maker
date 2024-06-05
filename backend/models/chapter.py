from pydantic import BaseModel


class Chapter(BaseModel):
    book_id: str
    chapter_number: int
    created_at: int
    chapter_name: str | None = None
    summary: str | None = None
    content: str | None = None
