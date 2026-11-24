import re


def validate_required(reference, required_fields):
    if any(not reference.get(field) for field in required_fields):
        raise ValueError("Täytä kaikki pakolliset kentät.")


def validate_citation(reference):
    if not re.fullmatch("[A-Za-z0-9:_-]+", reference["citation_key"]):
        raise ValueError("Viiteavain sisältää virheellisiä merkkejä.")

    if not re.fullmatch("[0-9]{4}", reference["year"]):
        raise ValueError("Vuoden pitää olla nelinumeroinen.")

    reference["year"] = int(reference["year"])

    return reference


def validate_pages(citation):
    if not re.fullmatch("[0-9]*-[0-9]*|[0-9]*", citation["pages"]):
        raise ValueError("Sivu numerot ei ole muotoa 1-12 tai 15")


def validate_article(article):
    validate_required(
        article, ("citation_key", "author", "title", "journal", "year", "type")
    )

    return validate_citation(article)


def validate_book(book):
    validate_required(book, ("citation_key", "author", "title", "year", "type"))
    validate_pages(book)

    if not re.fullmatch("[0-9]*", book["edition"]):
        raise ValueError("Painoksen pitäisi olla numero")

    book["edition"] = int(book["edition"])

    return validate_citation(book)


def validate_conference_article(conference_article):
    validate_required(
        conference_article,
        ("citation_key", "author", "title", "year", "conference_name", "city", "type"),
    )

    return validate_citation(conference_article)