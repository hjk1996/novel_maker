from pydantic import BaseModel


class Chapter(BaseModel):
    chapter_name: str | None = None
    summary: str | None = None
    content: str


class Book(BaseModel):
    id: str
    user_id: str
    title: str
    book_language: str | None = None
    cover_url: str | None = None
    genres: list[str]
    created_at: int
    chapters: list[Chapter] = []
    
    def get_story(self) -> str:
        story = ""        
        for i, ch in enumerate(self.chapters):
            story += f"Chapter {i+1}. <{ch.chapter_name if ch.chapter_name else "Untitled"}>" + "\n"
            story += ch.summary if ch.summary is not None else ch.content + "\n"
        return story
             



