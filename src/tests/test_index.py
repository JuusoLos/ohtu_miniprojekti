import pytest
from config import app, db
from db_helper import setup_db
from repositories.citation_repository import create_article

@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path / 'test.db'}"

    assert "test.db" in app.config["SQLALCHEMY_DATABASE_URI"]

    with app.app_context():
        setup_db()
        with app.test_client() as client:
            yield client
        db.session.remove()

def get_home(client):
    response = client.get("/")
    assert response.status_code == 200
    return response.get_data(as_text=True)

def test_renders_heading_and_new_article_link(client):
    html = get_home(client)
    assert "Lähteet" in html
    assert 'href="/citations/new"' in html

def test_empty_list_has_no_cards(client):
    html = get_home(client)
    assert "Ei lisättyjä lähteitä." in html
    assert 'class="source-card"' not in html


def test_two_articles_are_separate_compact_cards(client):
    articles = (
        {
            "citation_key": "TST1",
            "author": "Testikirjoittaja",
            "title": "Ensimmäinen otsikko",
            "journal": "Testijulkaisu",
            "year": 2026,
            "type": "article",
        },
        {
            "citation_key": "TST2",
            "author": "Testikirjoittaja",
            "title": "Toinen otsikko",
            "journal": "Testijulkaisu",
            "year": 2026,
            "type": "article",
        },
    )

    with app.app_context():
        for article in articles:
            create_article(article)

    html = get_home(client)
    assert html.count('class="source-card"') == 2
    for value in ("Ensimmäinen otsikko", "Toinen otsikko", "Testikirjoittaja", "2026"):
        assert value in html
    for extra in ("TST1", "TST2", "Otsikko:", "Viiteavain:",
                  "Julkaisu:", "Tyyppi:", "Testijulkaisu"):
        assert extra not in html
    assert 'href="/citations/' in html


def test_card_stylesheet_is_served(client):
    response = client.get("/static/source_cards.css")
    assert response.status_code == 200
    assert b".source-card" in response.data
