from fastapi import APIRouter
from pydantic import BaseModel
from app.services.api_reserchBooks import isbn_research, search_by_title, search_by_author

router = APIRouter()

class ISBNResearch(BaseModel):
    isbn_code: str

class TitleReserch(BaseModel):
    title: str

class AuthorResearch(BaseModel):
    authorName: str

@router.post("/isbn")
async def register(data: ISBNResearch):
    return await isbn_research(data.isbn_code)

@router.post("/title")
async def title(data: TitleReserch):
    return await search_by_title(data.title)

@router.post("/author")
async def author(data: AuthorResearch):
    return await search_by_author(data.authorName)
