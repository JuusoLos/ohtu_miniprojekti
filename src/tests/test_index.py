import pytest
from sqlalchemy import text
from config import app, db
from db_helper import setup_db

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
    assert 'href="/articles/new"' in html

def test_empty_list_has_no_cards(client):
    html = get_home(client)
    assert "Ei lisättyjä lähteitä." in html
    assert 'class="source-card"' not in html


def test_two_articles_are_separate_labeled_cards(client):
    with app.app_context():
        query = text(
            "INSERT INTO articles "
            "(citation_key, author, title, journal, year) "
            "VALUES (:citation_key, :author, :title, :journal, :year)"
        )
        for key, title in (("TST1", "Ensimmäinen otsikko"),
                           ("TST2", "Toinen otsikko")):
            db.session.execute(query, {
                "citation_key": key,
                "author": "Testikirjoittaja",
                "title": title,
                "journal": "Testijulkaisu",
                "year": 2026,
            })
        db.session.commit()

    html = get_home(client)
    assert html.count('class="source-card"') == 2
    for value in ("Ensimmäinen otsikko", "Toinen otsikko", "TST1", "TST2"):
        assert value in html
    for label in ("Otsikko:", "Kirjoittaja:", "Julkaisu:", "Vuosi:", "Viiteavain:"):
        assert label in html


def test_card_stylesheet_is_served(client):
    response = client.get("/static/source_cards.css")
    assert response.status_code == 200
    assert b".source-card" in response.data
