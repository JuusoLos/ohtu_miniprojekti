import pytest

from config import app, db
from db_helper import setup_db
from repositories.citation_repository import create_article, get_citations


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path / 'test.db'}"

    with app.app_context():
        setup_db()
        with app.test_client() as test_client:
            yield test_client
        db.session.remove()


def save_citations(*citation_keys):
    with app.app_context():
        for citation_key in citation_keys:
            create_article(
                {
                    "citation_key": citation_key,
                    "author": "Test author",
                    "title": f"Title {citation_key}",
                    "journal": "Test journal",
                    "year": 2026,
                    "type": "article",
                }
            )
        return {
            citation.citation_key: citation.id
            for citation in get_citations()
        }


def saved_citation_keys():
    with app.app_context():
        return {citation.citation_key for citation in get_citations()}


def test_delete_button_is_only_shown_when_citations_are_saved(client):
    empty_page = client.get("/")

    assert empty_page.status_code == 200
    assert b'id="delete-citations-button"' not in empty_page.data

    save_citations("FIRST")
    page_with_citation = client.get("/")

    assert page_with_citation.status_code == 200
    assert b'id="delete-citations-button"' in page_with_citation.data


def test_deleting_a_single_citation_removes_it(client):
    citation_ids = save_citations("FIRST")

    response = client.post(
        "/citations/delete",
        data={"citation_ids": str(citation_ids["FIRST"])},
    )

    assert response.status_code == 302
    assert saved_citation_keys() == set()


def test_deleting_one_of_multiple_citations_keeps_the_others(client):
    citation_ids = save_citations("FIRST", "SECOND", "THIRD")

    response = client.post(
        "/citations/delete",
        data={"citation_ids": str(citation_ids["SECOND"])},
    )

    assert response.status_code == 302
    assert saved_citation_keys() == {"FIRST", "THIRD"}


def test_deleting_multiple_citations_removes_all_checked_citations(client):
    citation_ids = save_citations("FIRST", "SECOND", "THIRD")

    response = client.post(
        "/citations/delete",
        data={
            "citation_ids": [
                str(citation_ids["FIRST"]),
                str(citation_ids["THIRD"]),
            ]
        },
    )

    assert response.status_code == 302
    assert saved_citation_keys() == {"SECOND"}


def test_deleting_with_no_checked_citations_changes_nothing(client):
    save_citations("FIRST", "SECOND")

    response = client.post("/citations/delete", data={})

    assert response.status_code == 302
    assert saved_citation_keys() == {"FIRST", "SECOND"}