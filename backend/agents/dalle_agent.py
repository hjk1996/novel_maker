import os

from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper


from models import Book


class DallEAgent:
    _prompt = """
    Generate a book cover image that matches the following book content.
    
    {content}
    """

    def __init__(self) -> None:

        self.image_generator = DallEAPIWrapper()

    def __call__(self, book: Book) -> str:
        image_url = self.image_generator.run(self._prompt.format(content=book.get_story_xml()))
        return image_url