import os
import dotenv

dotenv.load_dotenv()


from fastapi import FastAPI


from routers import books_router
from chat_models import Choices, NextStory
from chat_agents import ChoicesAgent, NextStoryAgent


app = FastAPI()
app.include_router(books_router)




if __name__ == "__main__":
    dotenv.load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("MODEL")
    choices_max_tokens = os.getenv("CHOICES_MAX_TOKENS")
    temperature = os.getenv("TEMPERATURE")

    choices_agent = ChoicesAgent(
        api_key=api_key,
        model=model,
        max_tokens=choices_max_tokens,
        temperature=temperature,
    )

    next_story_agent = NextStoryAgent(
        api_key=api_key,
        model=model,
        max_tokens=choices_max_tokens,
        temperature=temperature,
    )

    story = None
    while True:
        if story is None:
            story = input("Please enter the first line of the story: ")

        choices: Choices = choices_agent(story)
        print(f"1. {choices.choice_1}")
        print(f"2. {choices.choice_2}")
        print(f"3. {choices.choice_3}")
        print(f"4. {choices.choice_4}")
        print("\n")
        index = int(input("Please enter the index of the choice: "))
        next_story: NextStory = next_story_agent(
            previous_story=story, choice=choices[index]
        )
        story += "\n" + next_story.content
        print(story, "\n")
