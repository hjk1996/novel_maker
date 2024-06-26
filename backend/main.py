import dotenv
import logging


dotenv.load_dotenv()


from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import books_router, chapters_router, auth_router, generation_router




app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unexpected error occurred: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


@app.get("/health-check",
        status_code=status.HTTP_200_OK
        )
async def health_check():
    return {"status": "ok"}    


app.include_router(books_router)
app.include_router(chapters_router)
app.include_router(auth_router)
app.include_router(generation_router)