from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

_NUM_WORDS = {
    1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
    6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
    11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen",
    16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen", 20: "Twenty",
    21: "Twenty-one", 22: "Twenty-two", 23: "Twenty-three", 24: "Twenty-four",
    25: "Twenty-five", 26: "Twenty-six", 27: "Twenty-seven", 28: "Twenty-eight",
    29: "Twenty-nine", 30: "Thirty", 31: "Thirty-one", 32: "Thirty-two",
    33: "Thirty-three", 34: "Thirty-four", 35: "Thirty-five", 36: "Thirty-six",
    37: "Thirty-seven", 38: "Thirty-eight", 39: "Thirty-nine", 40: "Forty",
    41: "Forty-one", 42: "Forty-two", 43: "Forty-three", 44: "Forty-four",
    45: "Forty-five", 46: "Forty-six", 47: "Forty-seven", 48: "Forty-eight",
    49: "Forty-nine", 50: "Fifty",
    51: "Fifty-one", 52: "Fifty-two", 53: "Fifty-three", 54: "Fifty-four",
    55: "Fifty-five", 56: "Fifty-six", 57: "Fifty-seven", 58: "Fifty-eight",
    59: "Fifty-nine", 60: "Sixty", 61: "Sixty-one", 62: "Sixty-two",
    63: "Sixty-three", 64: "Sixty-four", 65: "Sixty-five", 66: "Sixty-six",
    67: "Sixty-seven", 68: "Sixty-eight", 69: "Sixty-nine", 70: "Seventy",
    71: "Seventy-one", 72: "Seventy-two", 73: "Seventy-three", 74: "Seventy-four",
    75: "Seventy-five", 76: "Seventy-six", 77: "Seventy-seven", 78: "Seventy-eight",
    79: "Seventy-nine", 80: "Eighty", 81: "Eighty-one", 82: "Eighty-two",
    83: "Eighty-three", 84: "Eighty-four", 85: "Eighty-five", 86: "Eighty-six",
    87: "Eighty-seven", 88: "Eighty-eight", 89: "Eighty-nine", 90: "Ninety",
    91: "Ninety-one", 92: "Ninety-two", 93: "Ninety-three", 94: "Ninety-four",
    95: "Ninety-five", 96: "Ninety-six", 97: "Ninety-seven", 98: "Ninety-eight",
    99: "Ninety-nine", 100: "One hundred",
    101: "One hundred one", 102: "One hundred two", 103: "One hundred three",
    104: "One hundred four", 105: "One hundred five", 106: "One hundred six",
    107: "One hundred seven", 108: "One hundred eight", 109: "One hundred nine",
    110: "One hundred ten", 111: "One hundred eleven", 112: "One hundred twelve",
    113: "One hundred thirteen", 114: "One hundred fourteen", 115: "One hundred fifteen",
    116: "One hundred sixteen", 117: "One hundred seventeen", 118: "One hundred eighteen",
    119: "One hundred nineteen", 120: "One hundred twenty",
    121: "One hundred twenty-one", 122: "One hundred twenty-two",
    123: "One hundred twenty-three", 124: "One hundred twenty-four",
    125: "One hundred twenty-five", 126: "One hundred twenty-six",
    127: "One hundred twenty-seven", 128: "One hundred twenty-eight",
    129: "One hundred twenty-nine", 130: "One hundred thirty",
    131: "One hundred thirty-one", 132: "One hundred thirty-two",
    133: "One hundred thirty-three", 134: "One hundred thirty-four",
    135: "One hundred thirty-five", 136: "One hundred thirty-six",
    137: "One hundred thirty-seven", 138: "One hundred thirty-eight",
    139: "One hundred thirty-nine", 140: "One hundred forty",
    141: "One hundred forty-one", 142: "One hundred forty-two",
    143: "One hundred forty-three", 144: "One hundred forty-four",
    145: "One hundred forty-five", 146: "One hundred forty-six",
    147: "One hundred forty-seven", 148: "One hundred forty-eight",
    149: "One hundred forty-nine", 150: "One hundred fifty",
    151: "One hundred fifty-one", 152: "One hundred fifty-two",
    153: "One hundred fifty-three", 154: "One hundred fifty-four",
    155: "One hundred fifty-five", 156: "One hundred fifty-six",
    157: "One hundred fifty-seven", 158: "One hundred fifty-eight",
    159: "One hundred fifty-nine", 160: "One hundred sixty",
    161: "One hundred sixty-one", 162: "One hundred sixty-two",
    163: "One hundred sixty-three", 164: "One hundred sixty-four",
    165: "One hundred sixty-five", 166: "One hundred sixty-six",
    167: "One hundred sixty-seven", 168: "One hundred sixty-eight",
    169: "One hundred sixty-nine", 170: "One hundred seventy",
    171: "One hundred seventy-one", 172: "One hundred seventy-two",
    173: "One hundred seventy-three", 174: "One hundred seventy-four",
    175: "One hundred seventy-five", 176: "One hundred seventy-six",
}


def _number_to_words(n: int) -> str:
    if n in _NUM_WORDS:
        return _NUM_WORDS[n]
    return str(n)


def _make_spoken_reference(chapter: int, verse: int) -> str:
    return f"{_number_to_words(chapter)} {_number_to_words(verse)}".lower().capitalize()


@dataclass(frozen=True)
class VerseRecord:
    reference: str
    spoken_reference: str
    text: str
    book: str
    chapter: int
    verse: int
    global_index: int


@dataclass(frozen=True)
class BookInfo:
    name: str
    total_verses: int
    chapters: int


class BibleDataProvider:
    """Loads Bible data from a JSON file and provides verse lookups."""

    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            data_path = Path(__file__).parent.parent / "data" / "kjv.json"
        self._data_path = data_path
        self._books: dict[str, list[VerseRecord]] = {}
        self._book_names: list[str] = []
        self._loaded = False

    def _ensure_loaded(self):
        if not self._loaded:
            self._load()

    def _load(self):
        with open(self._data_path, "r") as f:
            raw = json.load(f)

        for book_data in raw:
            book_name = book_data["book"]
            self._book_names.append(book_name)
            verses = []
            global_index = 0
            for chapter_data in book_data["chapters"]:
                chapter_num = int(chapter_data["chapter"])
                for verse_data in chapter_data["verses"]:
                    verse_num = int(verse_data["verse"])
                    reference = f"{book_name} {chapter_num}:{verse_num}"
                    spoken = _make_spoken_reference(chapter_num, verse_num)
                    verses.append(VerseRecord(
                        reference=reference,
                        spoken_reference=spoken,
                        text=verse_data["text"],
                        book=book_name,
                        chapter=chapter_num,
                        verse=verse_num,
                        global_index=global_index,
                    ))
                    global_index += 1
            self._books[book_name.lower()] = verses

        self._loaded = True

    def get_books(self) -> list[str]:
        """Return list of all book names."""
        self._ensure_loaded()
        return list(self._book_names)

    def get_book_info(self, book: str) -> BookInfo:
        """Return metadata about a book."""
        self._ensure_loaded()
        verses = self._get_book_verses(book)
        chapters = len(set(v.chapter for v in verses))
        return BookInfo(name=verses[0].book, total_verses=len(verses), chapters=chapters)

    def get_verse(self, book: str, chapter: int, verse: int) -> VerseRecord:
        """Look up a single verse."""
        self._ensure_loaded()
        verses = self._get_book_verses(book)
        for v in verses:
            if v.chapter == chapter and v.verse == verse:
                return v
        raise ValueError(f"Verse not found: {book} {chapter}:{verse}")

    def get_verse_range(
        self,
        book: str,
        chapter_start: int,
        verse_start: int,
        chapter_end: int,
        verse_end: int,
    ) -> list[VerseRecord]:
        """Return all verses in a range (inclusive)."""
        self._ensure_loaded()
        verses = self._get_book_verses(book)
        start_idx = None
        end_idx = None
        for i, v in enumerate(verses):
            if v.chapter == chapter_start and v.verse == verse_start:
                start_idx = i
            if v.chapter == chapter_end and v.verse == verse_end:
                end_idx = i
                break
        if start_idx is None or end_idx is None:
            raise ValueError(
                f"Range not found: {book} {chapter_start}:{verse_start} - {chapter_end}:{verse_end}"
            )
        return verses[start_idx : end_idx + 1]

    def get_verses_by_index(self, book: str, start_index: int, end_index: int) -> list[VerseRecord]:
        """Return verses by global_index range (inclusive)."""
        self._ensure_loaded()
        verses = self._get_book_verses(book)
        if start_index < 0 or end_index >= len(verses):
            raise ValueError(
                f"Index out of range: {start_index}-{end_index} (book has {len(verses)} verses)"
            )
        return verses[start_index : end_index + 1]

    def get_all_verses(self, book: str) -> list[VerseRecord]:
        """Return all verses for a book."""
        self._ensure_loaded()
        return list(self._get_book_verses(book))

    def _get_book_verses(self, book: str) -> list[VerseRecord]:
        key = book.lower()
        if key not in self._books:
            raise ValueError(f"Book not found: {book}")
        return self._books[key]


# Singleton instance
bible_data = BibleDataProvider()
