from app.utils.supabase_client import supabase
from datetime import datetime


async def database_books(page: int, limit: int, user_id: str = None, filters: dict = {}):
    try:
        data = {}
        filters = filters.dict(exclude_none=True) if filters else {}
        
        # Inizio query
        query = supabase.table("books").select("*", count="exact")

        # Applica i filtri in modo sicuro
        if filters.get("publisher"):
            query = query.eq("publisher", filters["publisher"])

        if filters.get("author"):
            query = query.ilike("author", f"%{filters['author']}%")

        if filters.get("title"):
            query = query.ilike("title", f"%{filters['title']}%")
        
        # Paginazione (0-based)
        from_index = (page - 1) * limit
        to_index = from_index + limit - 1
        query = query.range(from_index, to_index)

        books_response = query.execute()
        data["books"] = books_response.data
        data["count"] = books_response.count

        # Se richiesto, includi lista libri posseduti
        if user_id:
            books_owned = supabase.table("user_library") \
                .select("book_id") \
                .eq("user_id", user_id) \
                .execute()

            data["books_owned"] = [item["book_id"] for item in books_owned.data]

        return data

    except Exception as e:
        return {"error": str(e)}
    
async def add_book_on_library(book_id: str, user_id: str):
    try: 
        # Verifica se esiste ancora prima di inserire (per concorrenza)
        recheck = supabase.table("user_library").select("*").eq("user_id", user_id).eq("book_id", book_id).execute()
                
        book_data = {
            "user_id": user_id,
            "book_id": book_id
        }

        if not recheck.data:
            # Salva nel DB se non presente
            supabase.table("user_library").insert(book_data).execute()
            return {"result": False}

        return {"result": True}
    except Exception as e:
        return {"error": str(e), "result": False}
    
