from fastapi import APIRouter



router = APIRouter()


@router.get("/users/{user_id}/books/{book_id}/chapters")
def get_chapters(): ...


@router.get("/users/{user_id}/books/{book_id}/chapters/{chapter}")
def get_chapter(): ...


@router.post("/users/{user_id}/books/{book_id}/chapters/{chapter}")
def create_chapter(): ...


@router.delete("/users/{user_id}/books/{book_id}/chapters/{chapter}")
def delete_chapter(): ...
