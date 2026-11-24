import inspect
from sqlalchemy import text
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
    result = db.session.execute(sql)
    rows = result.fetchall()
    
    citations = [] 
    for row in rows:
        match row[-1]:
            case "article":
                citations.append(row_to_model(Article, row))
            case "book":
                citations.append(Book, row)
            case "conference":
                citations.append(ConferenceArticle, row)    

    return citations

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