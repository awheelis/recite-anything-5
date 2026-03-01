from fastapi import APIRouter, HTTPException, Query

from app.modules.bible_data_provider import bible_data
from app.schemas.bible import VerseResponse, BookInfoResponse

router = APIRouter()


@router.get("/books", response_model=list[str])
def list_books():
    return bible_data.get_books()


@router.get("/books/{book}", response_model=BookInfoResponse)
def get_book_info(book: str):
    try:
        info = bible_data.get_book_info(book)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return BookInfoResponse(name=info.name, total_verses=info.total_verses, chapters=info.chapters)


@router.get("/verse/{book}/{chapter}/{verse}", response_model=VerseResponse)
def get_verse(book: str, chapter: int, verse: int):
    try:
        v = bible_data.get_verse(book, chapter, verse)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return VerseResponse(
        reference=v.reference, spoken_reference=v.spoken_reference,
        text=v.text, book=v.book, chapter=v.chapter, verse=v.verse,
        global_index=v.global_index,
    )


@router.get("/verses/{book}", response_model=list[VerseResponse])
def get_verse_range(
    book: str,
    start_index: int = Query(ge=0),
    end_index: int = Query(ge=0),
):
    try:
        verses = bible_data.get_verses_by_index(book, start_index, end_index)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return [
        VerseResponse(
            reference=v.reference, spoken_reference=v.spoken_reference,
            text=v.text, book=v.book, chapter=v.chapter, verse=v.verse,
            global_index=v.global_index,
        )
        for v in verses
    ]
