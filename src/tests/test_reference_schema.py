from typing import Any


import sqlite3
import unittest
from pathlib import Path

SCHEMA = Path(__file__).resolve().parents[1] / "schema.sql"

class ReferenceSchemaTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.executescript(
            SCHEMA.read_text(encoding="utf-8")
        )

    def tearDown(self):
        self.connection.close()

    def test_article_can_be_saved(self):
        self.connection.execute(
            "INSERT INTO references"
            "(citation_key, author, title, journal, year, type)"
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("CBH91", "Collins", "Test article", "Journal", 1991, "article"),
        )

        result = self.connection.execute(
            "SELECT title FROM references WHERE citation_key = ?",
            ("CBH91",),
        ).fetchone()

        self.assertEqual(result[0], "Test article")

    def test_book_can_be_saved(self):
        self.connection.execute(
            "INSERT INTO references"
            "(citation_key, author, title, year, pages, publisher, edition, type)"
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("knuth1997art", "Donald E. Knuth", "The Art of Computer Programming, Volume 1: Fundamental Algorithms", 1997, "672", "Addison-Wesley", 3, "book")
        )

        result = self.connection.execute(
            "SELECT title FROM references WHERE citation_key = ?",
            ("knuth1997art",),
        ).fetchone()

        self.assertEqual(result[0], "The Art of Computer Programming, Volume 1: Fundamental Algorithms")

    def test_conference_article_can_be_saved(self):
        self.connection.execute(
            "INSERT INTO references"
            "(citation_key, author, title, journal, year, pages, conference_name, city, type)"
            ("smith2021deep", "John A. Smith", "Deep Learning Approaches for Medical Image Segmentation", "IEEE Transactions on Medical Imaging", 2021, "1123-1136", "International Conference on Medical Image Computing", "Helsinki", "conference_article")
        )

        result = self.connection.execute(
            "SELECT title FROM references WHERE citation_key = ?",
            ("smith2021deep",),
        ).fetchone()

        self.assertEqual(result[0], "Deep Learning Approaches for Medical Image Segmentation")

        

    def test_citation_key_is_unique(self):
        sql = (
            "INSERT INTO references "
            "(citation_key, author, title, journal, year, type) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        values = ("CBH91", "Author", "Title", "Journal", 1991, "article")

        self.connection.execute(sql, values)

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(sql, values)

    def test_title_is_required(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO references "
                "(citation_key, author, title, journal, year) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("TEST", "Author", None, "Journal", 2026, "article"),
            )