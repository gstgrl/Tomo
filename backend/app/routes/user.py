from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.services.user_functions import account_details, library_account, update_account, update_book

router = APIRouter()

class AccountUpdates(BaseModel):
    uid: str  # Obbligatorio per identificare l’utente
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    avatar_path: Optional[str] = None

class FilterModel(BaseModel):
    status: Optional[str] = None

class UpdatesModel(BaseModel):
    status: Optional[str] = None
    current_reading_page: Optional[str] = None
    rating: Optional[str] = None
    personal_notes: Optional[str] = None

class RequestModel(BaseModel):
    page: int
    limit: int
    user_id: str
    filters: Optional[FilterModel] = None

class BookUpdate(BaseModel):
    book_id: str
    user_id: str
    update_date: datetime
    updates: Optional[UpdatesModel] = None

@router.get("/account")
async def fetch_account_details(uid: str):
    return await account_details(uid)

@router.patch("/edit_account")
async def update_account_details(request: AccountUpdates):
    return await update_account(request.uid, request.name, request.surname, request.email, request.avatar_path)

@router.post("/library") 
async def books_account(payload: RequestModel):
    return await library_account(payload.page, payload.limit, payload.user_id, payload.filters)

@router.patch("/updateBook")
async def update_personal_book(payload: BookUpdate):
    return await update_book(payload.book_id, payload.user_id, payload.update_date, payload.updates)