import unittest

from entities.article import Article
from entities.book import Book
from entities.conference_article import ConferenceArticle


class TestEntities(unittest.TestCase):
    def test_book_to_dict(self):
        book = Book(
            id=1,
            citation_key="helsinki2026book",
            author="Test Author",
            title="Example Book",
            year=2026,
            pages="1–200",
            publisher="University of Helsinki",
            edition=1,
            type="book",
        )

        expected = {
            "id": 1,
            "citation_key": "helsinki2026book",
            "author": "Test Author",
            "title": "Example Book",
            "year": 2026,
            "pages": "1–200",
            "publisher": "University of Helsinki",
            "edition": 1,
            "type": "book",
        }

        self.assertEqual(book.to_dict(), expected)

    def test_article_to_dict(self):
        article = Article(
            id=2,
            citation_key="helsinki2026article",
            author="Test Author",
            title="Example Article",
            journal="University of Helsinki Journal",
            year=2026,
            type="article",
        )

        expected = {
            "id": 2,
            "citation_key": "helsinki2026article",
            "author": "Test Author",
            "title": "Example Article",
            "journal": "University of Helsinki Journal",
            "year": 2026,
            "type": "article",
        }

        self.assertEqual(article.to_dict(), expected)

    def test_conference_article_to_dict(self):
        article = ConferenceArticle(
            id=3,
            citation_key="helsinki2026conference",
            author="Test Author",
            title="Example Conference Article",
            year=2026,
            conference_name="Example Helsinki Conference",
            city="Helsinki",
            type="conference",
        )

        expected = {
            "id": 3,
            "citation_key": "helsinki2026conference",
            "author": "Test Author",
            "title": "Example Conference Article",
            "year": 2026,
            "conference_name": "Example Helsinki Conference",
            "city": "Helsinki",
            "type": "conference",
        }

        self.assertEqual(article.to_dict(), expected)