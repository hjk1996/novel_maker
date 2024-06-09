import os

from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import SystemMessage


from chat_models import Prompt
from models import Book


class DallEAgent:
    _prompt = """
    Create a prompt that can generate an image capturing the overall mood and content of the story presented below.
    
    {content}
    """

    def __init__(self) -> None:
        agent = ChatOpenAI(
            api_key=os.getenv("API_KEY"),
            model=os.getenv("MODEL"),
            max_tokens=os.getenv("NEXT_STORY_MAX_TOKENS"),
            temperature=os.getenv("TEMPERATURE"),
        )
        self.agent = agent.with_structured_output(Prompt)
        self.image_generator = DallEAPIWrapper()

    def __call__(self, book: Book) -> str:
        prompt: Prompt = self.agent.invoke(
            [SystemMessage(content=self._prompt.format(content=book.get_story_xml()))]
        )
        print(prompt)
        image_url = self.image_generator.run(prompt.prompt)
        return image_url
