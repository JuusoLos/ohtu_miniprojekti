from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from config import db


class DuplicateCitationKeyError(Exception):
    """Viiteavain on jo kaytossa."""


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