from datetime import datetime, timezone
from dotenv import load_dotenv
from app.utils.supabase_client import supabase
from app.utils.crypto import cifra_dato, decifra_dato

load_dotenv()


async def account_details(uid: str):
    try:
        query = supabase.table("users").select("*").eq("id", uid).single().execute()

        if query.data is None:
            return {"error": "Utente non trovato"}

        user = {}
        user["avatar_path"] = query.data.get("avatar_path")
        user["updated_at"] = query.data.get("updated_at")

        for field in ["name", "surname", "email"]:
            value = query.data.get(field)
            if value is not None:
                try:
                    decifrato = decifra_dato(value)
                    user[field] = decifrato
                    print(f"{field} decifrato:", decifrato)
                except Exception as e:
                    print(f"Errore nella decifratura del campo '{field}': {e}")

        return user  # ✅ RESTITUISCI QUESTO!

    except Exception as e:
        return {"error": str(e)}
    
async def update_account(user_id :str, name: str, surname: str, email: str, avatar_path: str):
    try: 
        update_fields = {}

        # Aggiungo e cifro solo i campi che non sono None
        if name is not None:
            update_fields["name"] = cifra_dato(name)
        if surname is not None:
            update_fields["surname"] = cifra_dato(surname)
        if email is not None:
            update_fields["email"] = cifra_dato(email)
        if avatar_path is not None:
            update_fields["avatar_path"] = avatar_path

        # Sempre aggiornare last_update
        update_fields["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        
        supabase.table("users").update(update_fields).eq("id", user_id).execute()

        return {"result": True}
    except Exception as e:
        return {"error": str(e), "result": False}
    
async def library_account(page: int, limit: int, user_id: str, filters: dict = {}):
    try:
        data = {}
        filters = filters.dict(exclude_none=True) if filters else {}
        
        # Inizio query
        query = supabase.table("user_library").select("*, book:book_id(*)", count="exact").eq("user_id", user_id )

        # Applica i filtri in modo sicuro
        if filters.get("status"):
            query = query.eq("status", filters['status'])

        # Paginazione (0-based)
        from_index = (page - 1) * limit
        to_index = from_index + limit - 1
        query = query.range(from_index, to_index)

        books_response = query.execute()
        data["books"] = books_response.data
        data["count"] = books_response.count
        data["total_pages"] = books_response.count / limit

        # 🔥 Aggiunta: riepilogo dei libri per status (ignorando i filtri attivi)
        status_summary_query = supabase.rpc("rpc_status_summary_with_ids", {"uid": user_id}).execute()
        status_summary = status_summary_query.data or []

        # Converte la lista in un dizionario
        data["status_summary"] = {
            row["status"]: {
            "count": row["count"],
            "ids": row["ids"],
            }
            for row in status_summary
        }

        return data

    except Exception as e:
        return {"error": str(e)}
    
async def update_book(book_id: str, user_id: str, update_date: datetime, updates: dict = {}):
    try: 
        # Verifica se esiste ancora prima di inserire (per concorrenza)
        recheck = supabase.table("user_library").select("*").eq("user_id", user_id).eq("book_id", book_id).execute()
        updates = updates.dict(exclude_none=True) if updates else {}
                
        data = {}

        data["last_update"] = update_date.isoformat()

        # Applica gli aggiornamenti presenti in modo sicuro
        if updates.get("status"):
            data["status"] = updates['status']

        if updates.get("current_reading_page"):
            data["current_reading_page"] = updates['current_reading_page']

        if updates.get("rating"):
            data["rating"] = updates['rating']

        if updates.get("personal_notes"):
            data["personal_notes"] = updates['personal_notes']

        data["last_update"] = update_date.isoformat()


        query = supabase.table("user_library").update(data).eq("book_id", book_id).eq("user_id", user_id)
        if recheck.data:
            # Salva nel DB se non presente
            query.execute()

        return {"result": True}
    except Exception as e:
        return {"error": str(e), "result": False}