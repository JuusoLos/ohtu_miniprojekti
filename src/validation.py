import re

FIELDS = ("citation_key", "author", "title", "journal", "year")


def validate_article(values):
    article = {
        field: str(values.get(field, "")).strip()
        for field in FIELDS
    }

    if any(not value for value in article.values()):
        raise ValueError("Täytä kaikki pakolliset kentät.")

    if not re.fullmatch(r"[A-Za-z0-9:_-]+", article["citation_key"]):
        raise ValueError("Viiteavain sisältää virheellisiä merkkejä.")

    if not re.fullmatch(r"[0-9]{4}", article["year"]):
        raise ValueError("Vuoden pitää olla nelinumeroinen.")

    article["year"] = int(article["year"])

    return article