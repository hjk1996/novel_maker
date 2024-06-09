import io

import requests

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


from di.auth import get_current_user
from di.agent import get_choices_agent, get_next_story_agent, get_dall_e_agent
from models import TokenPayload
from agents import NextStoryAgent, ChoicesAgent
from models import Book, Choices, NextStory
from agents import ChoicesAgent, NextStoryAgent, DallEAgent


router = APIRouter()


@router.post(
    "/generation/choices",
    response_model=Choices,
    status_code=status.HTTP_200_OK,
)
async def generate_choices(
    body: Book,
    current_user: TokenPayload = Depends(get_current_user),
    choices_agent: ChoicesAgent = Depends(get_choices_agent),
):
    story = body.get_story_xml()
    print(story)
    choices = await choices_agent(language=body.book_language, previous_story=story)
    return choices


class NextStoryBody(BaseModel):
    book: Book
    choice: str


@router.post(
    "/generation/next-story",
    response_model=NextStory,
    status_code=status.HTTP_200_OK,
)
async def generate_next_story(
    body: NextStoryBody,
    next_story_agent: NextStoryAgent = Depends(get_next_story_agent),
    current_user: TokenPayload = Depends(get_current_user),
):
    previous_story = body.book.get_story_xml()
    print(previous_story)
    next_story = await next_story_agent(
        previous_story=previous_story,
        choice=body.choice,
    )

    return next_story


@router.post(
    "/generation/book-cover",
    response_class=StreamingResponse,
    status_code=status.HTTP_200_OK,
)
def generate_book_cover(
    body: Book,
    current_user: TokenPayload = Depends(get_current_user),
    dall_e_agent: DallEAgent = Depends(get_dall_e_agent),
):
    image_url = dall_e_agent(body)
    response = requests.get(image_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve the image from the URL",
        )
    else:
        return StreamingResponse(
            content=io.BytesIO(response.content),
            media_type="image/png",  # Set the appropriate media type
        )
