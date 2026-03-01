from pydantic import BaseModel


class VerseRef(BaseModel):
    book: str
    chapter: int
    verse: int
    global_index: int


class VerseResponse(BaseModel):
    reference: str
    spoken_reference: str
    text: str
    book: str
    chapter: int
    verse: int
    global_index: int


class BookInfoResponse(BaseModel):
    name: str
    total_verses: int
    chapters: int
