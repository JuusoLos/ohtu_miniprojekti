import pytest
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
    assert 'href="/references/new"' in html