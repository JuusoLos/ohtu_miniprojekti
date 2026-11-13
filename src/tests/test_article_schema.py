import sqlite3
import unittest
from pathlib import Path

SCHEMA = Path(__file__).resolve().parents[1] / "schema.sql"


class ArticleSchemaTests(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.executescript(
            SCHEMA.read_text(encoding="utf-8")
        )

    def tearDown(self):
        self.connection.close()

    def test_article_can_be_saved(self):
        self.connection.execute(
            "INSERT INTO articles "
            "(citation_key, author, title, journal, year) "
            "VALUES (?, ?, ?, ?, ?)",
            ("CBH91", "Collins", "Test article", "Journal", 1991),
        )

        result = self.connection.execute(
            "SELECT title FROM articles WHERE citation_key = ?",
            ("CBH91",),
        ).fetchone()

        self.assertEqual(result[0], "Test article")

    def test_citation_key_is_unique(self):
        sql = (
            "INSERT INTO articles "
            "(citation_key, author, title, journal, year) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        values = ("CBH91", "Author", "Title", "Journal", 1991)

        self.connection.execute(sql, values)

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(sql, values)

    def test_title_is_required(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO articles "
                "(citation_key, author, title, journal, year) "
                "VALUES (?, ?, ?, ?, ?)",
                ("TEST", "Author", None, "Journal", 2026),
            )