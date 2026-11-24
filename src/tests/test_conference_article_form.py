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
from repositories.reference_repository import DuplicateCitationKeyError


class ConferenceArticleFormTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.valid_conference_article = {
            "citation_key": "smith2021deep",
            "author": "John A. Smith",
            "title": "Deep Learning Approaches for Medical Image Segmentation",
            "year": "2021",
            "pages": "1123-1136",
            "conference_name": "International Conference on Medical Image Computing",
            "city": "Helsinki",
        }

    def test_form_opens(self):
        response = self.client.get("/conference_articles/new")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="citation_key"', response.data)

    @patch("repositories.reference_repository.create_conference_article")
    def test_valid_conference_article_is_passed_to_storage(self, create_conference_article):
        response = self.client.post(
            "/conference_articles",
            data=self.valid_conference_article,
        )

        self.assertEqual(response.status_code, 303)

        create_conference_article.assert_called_once_with({
            "citation_key": "smith2021deep",
            "author": "John A. Smith",
            "title": "Deep Learning Approaches for Medical Image Segmentation",
            "year": 2021,
            "pages": "1123-1136",
            "conference_name": "International Conference on Medical Image Computing",
            "city": "Helsinki",
        })

    def test_missing_title_is_rejected(self):
        values = self.valid_conference_article.copy()
        values["title"] = ""

        response = self.client.post("/conference_articles", data=values)

        self.assertEqual(response.status_code, 400)

    def test_missing_conference_name_is_rejected(self):
        values = self.valid_conference_article.copy()
        values["conference_name"] = ""

        response = self.client.post("/conference_articles", data=values)

        self.assertEqual(response.status_code, 400)

    def test_invalid_year_is_rejected(self):
        values = self.valid_conference_article.copy()
        values["year"] = "abc"

        response = self.client.post("/conference_articles", data=values)

        self.assertEqual(response.status_code, 400)

    @patch("repositories.reference_repository.create_conference_article")
    def test_duplicate_key_shows_error(self, create_conference_article):
        create_conference_article.side_effect = DuplicateCitationKeyError()

        response = self.client.post(
            "/conference_articles",
            data=self.valid_conference_article,
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(
            "Viiteavain on jo käytössä".encode("utf-8"),
            response.data,
        )