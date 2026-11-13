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
import app as web_routes
from repositories.article_repository import DuplicateCitationKeyError


class ArticleFormTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.valid_article = {
            "citation_key": "CBH91",
            "author": "Collins",
            "title": "Test article",
            "journal": "Test Journal",
            "year": "1991",
        }

    def test_form_opens(self):
        response = self.client.get("/articles/new")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="citation_key"', response.data)

    @patch("repositories.article_repository.create_article")
    def test_valid_article_is_passed_to_storage(self, create_article):
        response = self.client.post(
            "/articles",
            data=self.valid_article,
        )

        self.assertEqual(response.status_code, 303)

        create_article.assert_called_once_with({
            "citation_key": "CBH91",
            "author": "Collins",
            "title": "Test article",
            "journal": "Test Journal",
            "year": 1991,
        })

    def test_missing_title_is_rejected(self):
        values = self.valid_article.copy()
        values["title"] = ""

        response = self.client.post("/articles", data=values)

        self.assertEqual(response.status_code, 400)

    def test_invalid_year_is_rejected(self):
        values = self.valid_article.copy()
        values["year"] = "abc"

        response = self.client.post("/articles", data=values)

        self.assertEqual(response.status_code, 400)

    @patch("repositories.article_repository.create_article")
    def test_duplicate_key_shows_error(self, create_article):
        create_article.side_effect = DuplicateCitationKeyError()

        response = self.client.post(
            "/articles",
            data=self.valid_article,
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(
            "Viiteavain on jo käytössä".encode("utf-8"),
            response.data,
        )