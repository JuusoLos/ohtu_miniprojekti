"""Lahteen tietosivun yksinkertaiset toiminnallisuustestit."""

import pytest
from config import app, db
from db_helper import setup_db
from repositories.citation_repository import create_article, create_book


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path / 'test.db'}"
    with app.app_context():
        setup_db()
        with app.test_client() as test_client:
            yield test_client
        db.session.remove()


def test_article_title_is_visible_on_page(client):
    with app.app_context():
        create_article({
            "citation_key": "TITLE2026",
            "author": "Testikirjoittaja",
            "title": "Näkyvä otsikko",
            "journal": "Testilehti",
            "year": 2026,
            "type": "article",
        })

    response = client.get("/citations/1")
    assert response.status_code == 200
    assert '<h1>Näkyvä otsikko</h1>' in response.get_data(as_text=True)


def test_book_edition_is_visible_without_pages(client):
    with app.app_context():
        create_book({
            "citation_key": "EDITION2026",
            "author": "Testikirjoittaja",
            "title": "Testikirja",
            "year": 2026,
            "pages": "",
            "publisher": "Testikustantaja",
            "edition": 2,
            "type": "book",
        })

    response = client.get("/citations/1")
    assert response.status_code == 200
    assert 'Painos:</strong> 2' in response.get_data(as_text=True)


def test_missing_citation_redirects_to_home(client):
    response = client.get("/citations/999999")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
