import pytest

from app.modules.bible_data_provider import BibleDataProvider, _make_spoken_reference


@pytest.fixture(scope="module")
def provider():
    p = BibleDataProvider()
    return p


class TestSpokenReference:
    def test_simple(self):
        assert _make_spoken_reference(1, 1) == "One one"

    def test_double_digit(self):
        assert _make_spoken_reference(6, 11) == "Six eleven"

    def test_large_numbers(self):
        assert _make_spoken_reference(27, 25) == "Twenty-seven twenty-five"

    def test_psalm_119(self):
        assert _make_spoken_reference(119, 176) == "One hundred nineteen one hundred seventy-six"


class TestGetBooks:
    def test_returns_list(self, provider):
        books = provider.get_books()
        assert isinstance(books, list)
        assert len(books) == 66

    def test_first_and_last(self, provider):
        books = provider.get_books()
        assert books[0] == "Genesis"
        assert books[-1] == "Revelation"


class TestGetBookInfo:
    def test_genesis(self, provider):
        info = provider.get_book_info("Genesis")
        assert info.name == "Genesis"
        assert info.chapters == 50
        assert info.total_verses > 1500

    def test_ephesians(self, provider):
        info = provider.get_book_info("Ephesians")
        assert info.name == "Ephesians"
        assert info.chapters == 6
        assert info.total_verses == 155

    def test_case_insensitive(self, provider):
        info = provider.get_book_info("genesis")
        assert info.name == "Genesis"

    def test_not_found(self, provider):
        with pytest.raises(ValueError, match="Book not found"):
            provider.get_book_info("NotABook")


class TestGetVerse:
    def test_genesis_1_1(self, provider):
        v = provider.get_verse("Genesis", 1, 1)
        assert v.reference == "Genesis 1:1"
        assert v.global_index == 0
        assert "In the beginning" in v.text

    def test_spoken_reference(self, provider):
        v = provider.get_verse("Ephesians", 6, 11)
        assert v.spoken_reference == "Six eleven"

    def test_not_found(self, provider):
        with pytest.raises(ValueError, match="Verse not found"):
            provider.get_verse("Genesis", 1, 999)


class TestGetVerseRange:
    def test_ephesians_1_1_to_1_3(self, provider):
        verses = provider.get_verse_range("Ephesians", 1, 1, 1, 3)
        assert len(verses) == 3
        assert verses[0].verse == 1
        assert verses[2].verse == 3

    def test_cross_chapter(self, provider):
        verses = provider.get_verse_range("Ephesians", 1, 22, 2, 2)
        assert len(verses) >= 3
        assert verses[0].chapter == 1
        assert verses[-1].chapter == 2


class TestGetVersesByIndex:
    def test_first_three(self, provider):
        verses = provider.get_verses_by_index("Genesis", 0, 2)
        assert len(verses) == 3
        assert verses[0].global_index == 0
        assert verses[2].global_index == 2

    def test_out_of_range(self, provider):
        with pytest.raises(ValueError, match="Index out of range"):
            provider.get_verses_by_index("Genesis", 0, 99999)


class TestGetAllVerses:
    def test_ephesians(self, provider):
        verses = provider.get_all_verses("Ephesians")
        assert len(verses) == 155
        assert verses[0].global_index == 0
        assert verses[-1].global_index == 154
