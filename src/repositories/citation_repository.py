import inspect
from sqlalchemy import bindparam, text
from sqlalchemy.exc import IntegrityError

from config import db

from entities.article import Article
from entities.book import Book
from entities.conference_article import ConferenceArticle

class DuplicateCitationKeyError(Exception):
    """Viiteavain on jo kaytossa."""

def row_to_model(cls, row):
    params = inspect.signature(cls.__init__).parameters
    fields = [p for p in params if p != "self"]
    data = row._mapping
    return cls(**{f: data[f] for f in fields})

def get_articles():
    sql = text("SELECT * FROM citations WHERE type='article'")
    result = db.session.execute(sql)
    articles = result.fetchall()
    return [Article(*row) for row in articles]

def get_books():
    sql = text("SELECT * FROM citations WHERE type='book'")
    result = db.session.execute(sql)
    books = result.fetchall()
    return [Book(*row) for row in books]

def get_conference_article():
    sql = text("SELECT * FROM citations WHERE type='conference_article'")
    result = db.session.execute(sql)
    conference_articles = result.fetchall()
    return [ConferenceArticle(*row) for row in conference_articles]

def get_citations():
    sql = text("SELECT * FROM citations")
    rows = db.session.execute(sql).fetchall()

    model_by_type = {
        "article": Article,
        "book": Book,
        "conference_article": ConferenceArticle,
    }

    citations = []
    for row in rows:
        model = model_by_type.get(row._mapping["type"])
        if model:
            citations.append(row_to_model(model, row))
    return citations

def get_citation_by_id(id: int) :
    sql = text("SELECT * FROM citations WHERE id = :id")
    row = db.session.execute(sql, {"id": id}).fetchone()
    if row is None:
        return None

    model_by_type = {
        "article": Article,
        "book": Book,
        "conference_article": ConferenceArticle,
    }
    model = model_by_type.get(row._mapping["type"])
    if model:
        return row_to_model(model, row)

def create_article(article):
    sql = text(
        "INSERT INTO citations "
        "(citation_key, author, title, journal, year, type) "
        "VALUES (:citation_key, :author, :title, :journal, :year, :type)"
    )

    try:
        db.session.execute(sql, article)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise DuplicateCitationKeyError from error

def create_book(book):
    sql = text(
        "INSERT INTO citations "
        "(citation_key, author, title, year, pages, publisher, edition, type) "
        "VALUES (:citation_key, :author, :title, :year, :pages, :publisher, :edition, :type)"
    )

    try:
        db.session.execute(sql, book)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise DuplicateCitationKeyError from error        

def create_conference_article(conference_article):
    sql = text(
        "INSERT INTO citations "
        "(citation_key, author, title, year, conference_name, city, type) "
        "VALUES (:citation_key, :author, :title, :year, :conference_name, :city, :type)"
    )

    try:
        db.session.execute(sql, conference_article)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise DuplicateCitationKeyError from error

def delete_citations(citation_ids):
    if not citation_ids:
        return

    sql = text(
        "DELETE FROM citations "
        "WHERE id IN :citation_ids"
    ).bindparams(bindparam("citation_ids", expanding=True))

    db.session.execute(sql, {"citation_ids": citation_ids})
    db.session.commit()