import os

from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from chat_models import NextStory


class NextStoryAgent:

    _prompt = """
    You are the AI designed for the 'Story Twist' function in a novel writing app. Your task is to craft the 'next story' of a story by taking into account the 'previous story' and the user's 'choice'. You will synthesize this information to create a seamless and engaging continuation of the plot.

    Input:

    previous_story: The last known state or event in the story, as written by the user.
    choice: The specific direction the user has chosen to take the story.

    Output:

    Generate a 'next story' that logically follows from the 'previous story' and the 'choice'.

    Rules:

    - The 'next story' should be a direct continuation that flows naturally from the 'choice'.
    - Maintain the tone and style of the original story, ensuring consistency in narrative voice.
    - Keep the 'next story' concise yet descriptive enough to inspire the user for further writing.
    - Avoid introducing new characters or elements that significantly deviate from the established plot.
    - The length of the 'next story' must not exceed 300 characters.
    - Ensure that the 'next situation' opens possibilities for further plot development.
    - Focus on advancing the plot or character development in a meaningful way.


    Now, let's start!

    previous_story: {previous_story}
    choice: {choice}
    """

    prompt_template = PromptTemplate(
        input_variables=["previous_story", "choice"], template=_prompt
    )

    def __init__(self) -> None:
        agent = ChatOpenAI(
            api_key=os.getenv("API_KEY"),
            model=os.getenv("MODEL"),
            max_tokens=os.getenv("NEXT_STORY_MAX_TOKENS"),
            temperature=os.getenv("TEMPERATURE"),
        )
        self.agent = agent.with_structured_output(NextStory)

    def __call__(self, previous_story: str, choice: str) -> NextStory:
        return self.agent.invoke(
            [
                SystemMessage(
                    content=self.prompt_template.format(
                        previous_story=previous_story, choice=choice
                    )
                )
            ]
        )
