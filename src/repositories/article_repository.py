from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from config import db

from entities.article import Article


class DuplicateCitationKeyError(Exception):
    """Viiteavain on jo kaytossa."""

def get_articles():
    sql = text("SELECT * FROM articles")
    result = db.session.execute(sql)
    articles = result.fetchall()
    return [Article(*row) for row in articles]

def create_article(article):
    sql = text(
        "INSERT INTO articles "
        "(citation_key, author, title, journal, year) "
        "VALUES (:citation_key, :author, :title, :journal, :year)"
    )

    try:
        db.session.execute(sql, article)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise DuplicateCitationKeyError from error