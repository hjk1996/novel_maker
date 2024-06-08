from pydantic import BaseModel
import xml.etree.ElementTree as ET


class Chapter(BaseModel):
    chapter_name: str
    content: str
    summary: str | None = None


class Book(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    genres: list[str]
    created_at: int
    book_language: str | None = None
    cover_url: str | None = None
    chapters: list[Chapter] = []

    def get_story_xml(self) -> str:
        root = ET.Element("book")

        title_element = ET.SubElement(root, "title")
        title_element.text = self.title

        description_element = ET.SubElement(root, "description")
        description_element.text = self.description

        genres_element = ET.SubElement(root, "genres")
        for genre in self.genres:
            genre_element = ET.SubElement(genres_element, "genre")
            genre_element.text = genre

        if self.book_language:
            language_element = ET.SubElement(root, "book_language")
            language_element.text = self.book_language

        chapters_element = ET.SubElement(root, "chapters")
        for i, ch in enumerate(self.chapters):
            chapter_element = ET.SubElement(chapters_element, "chapter")
            chapter_element.set("number", str(i + 1))
            chapter_name = ch.chapter_name if ch.chapter_name else "Untitled"
            chapter_element.set("name", chapter_name)
            content_element = ET.SubElement(chapter_element, "content")
            if ch.summary is not None:
                content_element.text = ch.summary
            else:
                content_element.text = ch.content

        last_paragraph = ET.SubElement(root, "last_paragraph")
        last_paragraph.text = self.chapters[-1].content[-200:]

        return ET.tostring(root, encoding="unicode")
