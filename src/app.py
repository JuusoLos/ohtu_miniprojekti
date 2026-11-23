from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from config import app, test_env
from repositories.reference_repository import get_references, create_book, create_article, create_conference_article, DuplicateCitationKeyError
from validation import validate_article

@app.route("/")
def index():
    return render_template(
        "index.html",
        references=get_references()
    ) 

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })


@app.route("/references/new", methods=["GET"])
def new_article():
    return render_template(
        "new_reference.html",
        values={},
        saved=request.args.get("saved") == "1",
    )


def add_reference(fields, validate_reference, create_reference):
    values = {
        field: request.form.get(field, "").strip()
        for field in fields
    }

    try:
        reference = validate_reference(values)
        create_reference(reference)

    except ValueError as error:
        return render_template(
            "new_reference.html",
            values=values,
            error=str(error),
        ), 400

    except DuplicateCitationKeyError:
        return render_template(
            "new_reference.html",
            values=values,
            error="Viiteavain on jo käytössä.",
        ), 409

    return redirect("/references/new?saved=1", code=303)

@app.route("/articles", methods=["POST"])
def add_article():
    return add_reference(("citation_key", "author", "title", "journal", "year", "type"), validate_article, create_article)

@app.route("/books", methods=["POST"])
def add_book():
    return add_reference(("citation_key", "author", "title", "year", "pages", "publisher", "type"),  validate_book, create_book)

@app.route("/conference_articles", methods=["POST"])
def add_book():
    return add_reference(("citation_key", "author", "title", "journal", "year", "pages", "conference_name", "city", "type"),  validate_book, create_book)

