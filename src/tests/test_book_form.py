import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC))

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-secret")

from config import app
from repositories.citation_repository import DuplicateCitationKeyError


class BookFormTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.valid_book = {
            "citation_key": "knuth1997art",
            "author": "Donald E. Knuth",
            "title": "The Art of Computer Programming, Volume 1: Fundamental Algorithms",
            "year": "1997",
            "pages": "672",
            "publisher": "Addison-Wesley",
            "edition":  3,
            "type": "book"
        }

    def test_form_opens(self):
        response = self.client.get("/citations/new")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="citation_key"', response.data)

    @patch("app.create_book")
    def test_valid_book_is_passed_to_storage(self, create_book):
        response = self.client.post(
            "/books",
            data=self.valid_book,
        )

        self.assertEqual(response.status_code, 303)

        create_book.assert_called_once_with({
            "citation_key": "knuth1997art",
            "author": "Donald E. Knuth",
            "title": "The Art of Computer Programming, Volume 1: Fundamental Algorithms",
            "year": 1997,
            "pages": "672",
            "publisher": "Addison-Wesley",
            "edition":  3,
            "type": "book"
        })

    def test_missing_title_is_rejected(self):
        values = self.valid_book.copy()
        values["title"] = ""

        response = self.client.post("/books", data=values)

        self.assertEqual(response.status_code, 400)

    def test_invalid_year_is_rejected(self):
        values = self.valid_book.copy()
        values["year"] = "abc"

        response = self.client.post("/books", data=values)

        self.assertEqual(response.status_code, 400)

    @patch("app.create_book")
    def test_duplicate_key_shows_error(self, create_book):
        create_book.side_effect = DuplicateCitationKeyError()

        response = self.client.post(
            "/books",
            data=self.valid_book,
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(
            "Viiteavain on jo käytössä".encode("utf-8"),
            response.data,
        )