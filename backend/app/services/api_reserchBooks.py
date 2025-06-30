import os
from datetime import datetime
import httpx
from dotenv import load_dotenv
from app.utils.supabase_client import supabase

load_dotenv()


async def isbn_research(isbn: str):
    # 1. Prova a cercare nel database
    query = supabase.table("books").select("*").eq("isbn", isbn).execute()

    if query.data and len(query.data) > 0:
        return {"source": "database", "data": query.data[0]}

    # 2. Altrimenti cerca su Google Books
    async with httpx.AsyncClient() as client:
        google_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        gb_response = await client.get(google_url)

        if gb_response.status_code == 200:
            gb_data = gb_response.json()
            if gb_data.get("totalItems", 0) > 0:
                item = gb_data["items"][0]  # ✅ Prendi il primo risultato
                volume_info = item.get("volumeInfo", {})

                # Trasforma in oggetto compatibile con il DB
                book_data = {
                    "title": volume_info.get("title", "Titolo sconosciuto"),
                    "author": ", ".join(volume_info.get("authors", ["Sconosciuto"])),
                    "isbn": isbn,
                    "page_count": volume_info.get("pageCount", 0),
                    "language": volume_info.get("language", "n/a"),
                    "cover_url": volume_info.get("imageLinks", {}).get("thumbnail", None),
                    "description": volume_info.get("description", ""),
                    "published_date": volume_info.get("publishedDate", ""),
                    "publisher": volume_info.get("publisher", ""),
                    "source": "googlebooks"
                }

                # 3. Inserisci nel DB se possibile
                response = supabase.table('books').insert(book_data).execute()

                if not response.data:
                    return {"error": "Errore di salvataggio"}

                return {"source": "googlebooks", "data": response.data[0]}

    # 4. Nessun risultato
    return {"error": "Nessun risultato trovato nel database o su Google Books"}

async def search_by_author(author_name: str):
    async with httpx.AsyncClient() as client:
        # 🔁 Fallback su Google Books
        gb_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author_name}"
        gb_response = await client.get(
            gb_url,
            params={"author_name": author_name.strip()}
        )

        if gb_response.status_code == 200 and gb_response.json().get("totalItems", 0) > 0:
            return {"source": "googlebooks", "data": gb_response.json()}

    return {"error": "Nessun risultato trovato con OpenLibrary o Google Books"}

async def search_by_title(title: str):
    # 1. Prova a cercare nel database
    query = supabase.table("books").select("*").eq("title", title).execute()

    if query.data and len(query.data) > 0:
        return {"source": "database", "total_results": len(query.data),"data": query.data}

    # 2. Altrimenti cerca su Google Books
    async with httpx.AsyncClient() as client:
        google_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
        gb_response = await client.get(google_url)

        if gb_response.status_code == 200 and gb_response.json().get("totalItems", 0) > 0:
            books_found = []

            for item in gb_response.json()["items"][:10]:  # max 5 risultati
                info = item.get("volumeInfo", {})
                isbn = info.get("industryIdentifiers", [{}])[0].get("identifier", "")
                
                book_data = {
                    "title": info.get("title", "Titolo sconosciuto"),
                    "author": ", ".join(info.get("authors", ["Sconosciuto"])),
                    "isbn": isbn,
                    "page_count": info.get("pageCount", 0),
                    "language": info.get("language", "n/a"),
                    "cover_url": info.get("imageLinks", {}).get("thumbnail", ""),
                    "description": info.get("description", ""),
                    "published_date": info.get("publishedDate", ""),
                    "publisher": info.get("publisher", ""),
                    "source": "googlebooks"
                }
                # Verifica se esiste ancora prima di inserire (per concorrenza)
                recheck = supabase.table("books").select("*").eq("isbn", isbn).execute()

                if not recheck.data:
                    # Salva nel DB se non presente
                    supabase.table("books").insert(book_data).execute()

                books_found.append(book_data)

            return {"source": "googlebooks", "total_results": len(books_found), "data": books_found}

    return {"error": "Nessun libro trovato"}