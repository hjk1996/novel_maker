import os

from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from chat_models import NextStory


class NextStoryAgent:

    _prompt = """
You are the AI for the 'Story Twist' feature in a novel writing app. Your task is to create the 'next story' segment based on the 'previous story' and the user's 'choice'. Use this information to craft a seamless and engaging plot continuation.

Input:

genres: The genre or genres of the story.
language: The language in which the book is written.
previous_story: The last known event in the story, written by the user.
choice: The specific direction the user has chosen for the story.

Rules:

- The 'next story' should directly continue from the 'choice' and the paragraph of the last chapter.
- Maintain the original story's tone and style for consistency.
- Keep the 'next story' concise but descriptive to inspire further writing.
- Avoid introducing new characters or elements that deviate from the plot.
- Do not generate chapter names or numbers.
- Limit the 'next story' to 300 characters.
- Ensure the 'next story' allows for further plot development.
- Focus on meaningful plot or character advancement.
- Focus on the "last_paragraph" attribute to generate story that ensure a natural continuation of the story.

Let's begin!




previous_story
```
{previous_story}
```
choice
```
{choice}
```
    """

    prompt_template = PromptTemplate(
        input_variables=["previous_story", "choice"], template=_prompt
    )

    def __init__(self, api_key) -> None:
        agent = ChatOpenAI(
            api_key=api_key,
            model=os.getenv("MODEL", "gpt-4o"),
            max_tokens=300,
            temperature=0.9,
        )
        self.agent = agent.with_structured_output(NextStory)

    async def __call__(self, previous_story: str, choice: str) -> NextStory:
        response = await self.agent.ainvoke(
            [
                SystemMessage(
                    content=self.prompt_template.format(
                        previous_story=previous_story,
                        choice=choice,
                    )
                )
            ]
        )
        return response
