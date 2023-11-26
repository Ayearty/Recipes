from flask_app import app
from flask import render_template, request, redirect,session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route("/recipes/new")
def form():
    recipes = Recipe.get_all()
    print(recipes)
    user = {
        "id" : session["user_id"]
    }
    return render_template("new_recipe.html", user = user)

@app.route("/create_recipe", methods=["POST"])
def new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect ("/recipes/new")
    data = {
        "name":request.form["name"],
        "under30":request.form["under30"],
        "date_made":request.form["date_made"],
        "creator_id":request.form['creator_id'],
        "description":request.form['description'],
        "instructions":request.form['instructions']
    }
    user = Recipe.save(data)
    session["creator_id"] = user
    return redirect('/recipes')

@app.route("/delete/<int:id>")
def delete(id):
    Recipe.delete(id)
    return redirect("/recipes")

@app.route("/edit/<int:id>")
def update(id):
    data = {
        "id" : id
    }
    recipe = Recipe.get_one(data)
    users = User.get_all()
    return render_template("edit_recipe.html", recipe = recipe, users = users)

@app.route("/update/recipe/<int:id>", methods=["POST"])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect (f"/edit/{id}")
    data = {
        "id":id,
        "name":request.form["name"],
        "under30":request.form["under30"],
        "date_made":request.form["date_made"],
        "description":request.form['description'],
        "instructions":request.form['instructions']
    }
    Recipe.update_one(data)
    return redirect(f"/show/recipe/{id}")

@app.route("/show/recipe/<int:id>")
def show_recipe(id):
    data = {
        'id' : id
    }
    user = {
        "id" : session["user_id"]
    }
    recipe = Recipe.get_one(data)
    logged_in_user = User.get_by_id(user)
    return render_template("recipe_card.html", recipe = recipe, logged_in_user = logged_in_user)
