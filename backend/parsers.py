from langchain.output_parsers import (
    PydanticOutputParser,
    StructuredOutputParser,
    ResponseSchema,
    CommaSeparatedListOutputParser
)
from models import Choices


def get_next_story_parser() -> StructuredOutputParser:
    return StructuredOutputParser.from_response_schemas(
        response_schemas=[
            ResponseSchema(
                name="next_story",
                type="string",
                description="Next situation of the story",
            ),
        ]
    )


def get_choices_parser() -> PydanticOutputParser:
    return PydanticOutputParser(
        pydantic_object=Choices,
    )