from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from config import app, test_env

@app.route("/")
def index():
    return render_template("index.html") 

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })


@app.route("/articles/new", methods=["GET"])
def new_article():
    return render_template(
        "new_article.html",
        values={},
        saved=request.args.get("saved") == "1",
    )


@app.route("/articles", methods=["POST"])
def add_article():
    from repositories.article_repository import (
        create_article,
        DuplicateCitationKeyError,
    )
    from validation import validate_article

    values = {
        field: request.form.get(field, "").strip()
        for field in ("citation_key", "author", "title", "journal", "year")
    }

    try:
        article = validate_article(values)
        create_article(article)

    except ValueError as error:
        return render_template(
            "new_article.html",
            values=values,
            error=str(error),
        ), 400

    except DuplicateCitationKeyError:
        return render_template(
            "new_article.html",
            values=values,
            error="Viiteavain on jo käytössä.",
        ), 409

    return redirect("/articles/new?saved=1", code=303)
