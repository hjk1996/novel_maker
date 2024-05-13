import os
from pprint import pprint

import dotenv
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.llms.openai import OpenAI
from langchain.output_parsers import (
    PydanticOutputParser,
    StructuredOutputParser,
    RetryWithErrorOutputParser,
)
from langchain.schema import SystemMessage

from parsers import get_choices_parser, get_next_story_parser
from templates import get_choices_system_template, get_next_story_system_template
from models import Choices

TEMPERATURE = 0.9
CHOICES_MAX_TOKENS = 200
NEXT_STORY_MAX_TOKENS = 300
MODEL = "gpt-4-1106-preview"


def create_choices_prompt_message(
    choices_system_template: PromptTemplate,
    choices_parser: PydanticOutputParser,
    previous_story: str,
) -> list[SystemMessage]:
    return [
        SystemMessage(
            content=choices_system_template.format(
                format_instruction=choices_parser.get_format_instructions(),
                input=previous_story,
            )
        )
    ]


def create_next_story_prompt_message(
    next_story_system_template: PromptTemplate,
    next_story_parser: StructuredOutputParser,
    previous_story: str,
    choice: str,
) -> list[SystemMessage]:
    return [
        SystemMessage(
            content=next_story_system_template.format(
                format_instruction=next_story_parser.get_format_instructions(),
                previous_story=previous_story,
                choice=choice,
            )
        )
    ]


if __name__ == "__main__":
    dotenv.load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    choices_chat = ChatOpenAI(
        api_key=api_key,
        model=MODEL,
        max_tokens=CHOICES_MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    next_story_chat = ChatOpenAI(
        api_key=api_key,
        model=MODEL,
        max_tokens=NEXT_STORY_MAX_TOKENS,
        temperature=TEMPERATURE,
    )

    choices_parser = get_choices_parser()
    next_story_parser = get_next_story_parser()

    choices_system_template = get_choices_system_template()
    next_story_system_template = get_next_story_system_template()

    story = None
    with get_openai_callback() as cb:
        while True:
            if story is None:
                story = input("Please enter the first line of the story: ")

            choices_prompt_message = create_choices_prompt_message(
                choices_system_template=choices_system_template,
                choices_parser=choices_parser,
                previous_story=story,
            )
            choice = choices_chat(messages=choices_prompt_message)

            parsed_choice: Choices = choices_parser.parse(choice.content)
            print(f"1. {parsed_choice.choice_1}")
            print(f"2. {parsed_choice.choice_2}")
            print(f"3. {parsed_choice.choice_3}")
            print(f"4. {parsed_choice.choice_4}")
            print(f"total cost: {cb.total_cost}", "\n")
            print("\n")
            index = int(input("Please enter the index of the choice: "))
            if index == 5:
                next_story_content = input("Next story: ")
                next_story = next_story_chat(
                    messages=create_next_story_prompt_message(
                        next_story_system_template=next_story_system_template,
                        next_story_parser=next_story_parser,
                        previous_story=story,
                        choice=next_story_content,
                    )
                )
            else:
                next_story = next_story_chat(
                    messages=create_next_story_prompt_message(
                        next_story_system_template=next_story_system_template,
                        next_story_parser=next_story_parser,
                        previous_story=story,
                        choice=parsed_choice[index],
                    )
                )
            parsed_next_story = next_story_parser.parse(next_story.content)
            story += "\n" + parsed_next_story["next_story"]
            print(story, "\n")
