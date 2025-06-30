from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.supabase import database_books, add_book_on_library

router = APIRouter()

class AddBookRequest(BaseModel):
    book_id: str
    user_id: str

class FilterModel(BaseModel):
    isbn: Optional[str] = None
    author: Optional[str] = None
    title: Optional[str] = None

class RequestModel(BaseModel):
    page: int
    limit: int
    user_id: str
    filters: Optional[FilterModel] = None

@router.post("/books")
async def all_books(payload: RequestModel):
    return await database_books(payload.page, payload.limit, payload.user_id, payload.filters)

@router.post("/addBook")
async def add_book_personal_library(request: AddBookRequest):
    return await add_book_on_library(request.book_id, request.user_id)


