from fastapi import APIRouter

from chat_agents import NextStoryAgent, ChoicesAgent


router = APIRouter()
next_stroy_agent = NextStoryAgent()
choices_agent = ChoicesAgent()


@router.get("/users/{user_id}")
def get_books(): ...


@router.get("/users/{user_id}/{book_id}")
def get_book(): ...


@router.post("/users/{user_id}/{book_id}/choices")
def create_choices(): ...


@router.post("/users/{user_id}/{book_id}/next-story")
def create_next_story(): ...
