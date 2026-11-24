import re

def validate_reference(reference):
    if not re.fullmatch("[A-Za-z0-9:_-]+", reference["citation_key"]):
        raise ValueError("Viiteavain sisältää virheellisiä merkkejä.")

    if not re.fullmatch("[0-9]{4}", reference["year"]):
        raise ValueError("Vuoden pitää olla nelinumeroinen.")

    reference["year"] = int(reference["year"])

    return reference

def validate_pages(reference):
    if not re.fullmatch("[0-9]*-[0-9]*|[0-9]*", reference["pages"]):
        raise ValueError("Sivu numerot ei ole muotoa 1-12 tai 15")

def validate_article(article):
    if any(not value for value in article.values()):
        raise ValueError("Täytä kaikki pakolliset kentät.")

    return validate_reference(article)

def validate_book(book):
    validate_pages(book)

    return validate_reference(book)

def validate_conference_article(conference_article):
    validate_pages()

    return validate_reference(conference_article)