from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from config import db

from entities.article import Article
from entities.book import Book
from entities.conference_article import ConferenceArticle

class DuplicateCitationKeyError(Exception):
    """Viiteavain on jo kaytossa."""

def get_articles():
    sql = text("SELECT * FROM references WHERE type='article'")
    result = db.session.execute(sql)
    articles = result.fetchall()
    return [Article(*row) for row in articles]

def get_books():
    sql = text("SELECT * FROM references WHERE type='book'")
    result = db.session.execute(sql)
    books = result.fetchall()
    return [Book(*row) for row in books]

def get_conference_article():
    sql = text("SELECT * FROM references WHERE type='conference'")
    result = db.session.execute(sql)
    conference_articles = result.fetchall()
    return [ConferenceArticle(*row) for row in conference_articles]

def get_references():
    sql = text("SELECT * FROM references")
    result = db.session.execute(sql)
    rows = result.fetchall()
    
    references = [] 
    for row in rows:
        match row[-1]:
            case "article":
                references.append(Article(*filter(row)))
            case "book":
                references.append(Book(*filter(row)))
            case "conference":
                references.append(ConferenceArticle(*filter(row)))    

    return references

def create_article(article):
    sql = text(
        "INSERT INTO references"
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
        "INSERT INTO references"
        "(citation_key, author, title, year, pages, publisher, type)"
        "VALUES (:citation_key, :author, :title, :year, :pages, :publisher, :type)"
    )

    try:
        db.session.execute(sql, book)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise DuplicateCitationKeyError from error        

def create_conference_article(conference_article):
    sql = text(
        "INSERT INTO references"
        "(citation_key, author, title, journal, year, pages, conference_name, city, type) "
        "VALUES (:citation_key, :author, :title, :journal, :year, :pages, :conference_name, :city, :type)"
    )

    try:
        db.session.execute(sql, conference_article)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise DuplicateCitationKeyError from error        