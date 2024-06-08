import os

from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from chat_models import Choices


class ChoicesAgent:

    _prompt = """
You are the AI of the 'Story Twist' novel writing app. In this app, your task is to provide users with four choices to influence the plot of their novel. Your role is to analyze the current plot and generate compelling choices that can take the story in different directions.

Rules:

- Analyze the previous situation of the novel.
- Generate four distinct choices that could logically follow from the current plot.
- Ensure the choices are diverse and cater to different story outcomes.
- Provide the choices in a clear and concise manner for the user to select from.
- Ensure the choices are brief and to the point, less than 40 characters each.
- Choices must be written in the provided language or the language of the book.
- Follow these specific guidelines for the choices:
    - The first choice should align closely with the current plot direction.
    - The second choice should offer a positive or optimistic turn.
    - The third choice should introduce a negative or challenging twist.
    - The fourth choice can be completely random or unexpected.
- Focus on the "last_paragraph" attribute to generate story that ensure a natural continuation of the story.

book_information
```
{previous_story}
```
"""

    prompt_template = PromptTemplate(
        input_variables=["previous_story"],
        template=_prompt,
    )

    def __init__(self) -> None:
        agent = ChatOpenAI(
            api_key=os.getenv("API_KEY"),
            model=os.getenv("MODEL"),
            max_tokens=os.getenv("CHOICES_MAX_TOKENS"),
            temperature=os.getenv("TEMPERATURE"),
        )
        self.agent = agent.with_structured_output(Choices)

    async def __call__(self, language: str, previous_story: str) -> Choices:
        response = await self.agent.ainvoke(
            [
                SystemMessage(
                    content=self.prompt_template.format(
                        language=language, previous_story=previous_story
                    )
                )
            ]
        )
        return response
