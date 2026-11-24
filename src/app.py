from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from config import app, test_env
from repositories.citation_repository import get_citations, create_book, create_article, create_conference_article, DuplicateCitationKeyError
from validation import validate_article, validate_book, validate_conference_article

@app.route("/")
def index():
    return render_template(
        "index.html",
        citations=get_citations()
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
    )


def add_citation(fields, validate_reference, create_reference):
    values = {
        field: request.form.get(field, "").strip()
        for field in fields
    }

    try:
        reference = validate_reference(values)
        create_reference(reference)

    except ValueError as error:
        return render_template(
            "new_citations.html",
            values=values,
            error=str(error),
        ), 400

    except DuplicateCitationKeyError:
        return render_template(
            "new_citations.html",
            values=values,
            error="Viiteavain on jo käytössä.",
        ), 409

    return redirect("/citations/new?saved=1", code=303)

@app.route("/articles", methods=["POST"])
def add_article():
    return add_citation(("citation_key", "author", "title", "journal", "year", "type"), validate_article, create_article)

@app.route("/books", methods=["POST"])
def add_book():
    return add_citation(("citation_key", "author", "title", "year", "pages", "publisher", "edition", "type"),  validate_book, create_book)

@app.route("/conference_articles", methods=["POST"])
def add_conference_article():
    return add_citation(("citation_key", "author", "title", "year", "conference_name", "city", "type"),  validate_conference_article, create_conference_article)

if __name__ == "__main__":
    app.run(port=5001)