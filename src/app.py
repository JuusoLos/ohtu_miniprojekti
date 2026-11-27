from flask import redirect, render_template, request, jsonify
from db_helper import reset_db
from config import app, test_env
from repositories.citation_repository import get_citation_by_id, get_citations, create_book, create_article, create_conference_article, DuplicateCitationKeyError
from validation import validate_article, validate_book, validate_conference_article

CITATION_TYPE_LABELS = {
    "article": "Artikkeli",
    "book": "Kirja",
    "conference_article": "Konferenssijulkaisu",
}

@app.route("/")
def index():
    return render_template(
        "index.html",
        citations=get_citations(),
        citation_type_labels=CITATION_TYPE_LABELS,
    ) 

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })


@app.route("/citations/new", methods=["GET"])
def new_article():
    return render_template(
        "new_citations.html",
        values={},
        saved=request.args.get("saved") == "1",
        type=request.args.get("type", "article")
    )


def add_citation(fields, validate_citation, create_citation, type):
    values = {
        field: request.form.get(field, "").strip()
        for field in fields
    }
    values["type"] = type

    try:
        citation = validate_citation(values)
        create_citation(citation)

    except ValueError as error:
        return render_template(
            "new_citations.html",
            values=values,
            error=str(error),
            type="article", 
        ), 400

    except DuplicateCitationKeyError:
        return render_template(
            "new_citations.html",
            values=values,
            error="Viiteavain on jo käytössä.",
            type="article",
        ), 409

    return redirect(f"/citations/new?saved=1&type={type}", code=303)

@app.route("/citations/delete", methods=["POST"])
def delete_citations():
    from repositories.citation_repository import delete_citations

    citation_ids = request.form.getlist("citation_ids")
    delete_citations([int(citation_id) for citation_id in citation_ids])
    return redirect("/")

@app.route("/articles", methods=["POST"])
def add_article():
    return add_citation(("citation_key", "author", "title", "journal", "year", "type"), validate_article, create_article, "article")

@app.route("/books", methods=["POST"])
def add_book():
    return add_citation(("citation_key", "author", "title", "year", "pages", "publisher", "edition", "type"),  validate_book, create_book, "book")

@app.route("/conference_articles", methods=["POST"])
def add_conference_article():
    return add_citation(("citation_key", "author", "title", "year", "conference_name", "city", "type"),  validate_conference_article, create_conference_article, "conference_article")

@app.route("/citations/<int:id>")
def citation(id: int):
    citation = get_citation_by_id(id)
    if citation:
        return render_template("citation_page.html", citation=citation)

    return redirect("/")    

if __name__ == "__main__":
    app.run()
