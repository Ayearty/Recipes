from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from pprint import pprint
from flask import flash

class Recipe:
    DB="recipes"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.creator_id = data['creator_id']
        self.description = data['description']
        self.instructions = data['instructions']
        self.user = None

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO recipes.recipes (name,description,instructions,creator_id,under30,date_made) 
        VALUES (%(name)s,%(description)s,%(instructions)s,%(creator_id)s,%(under30)s,%(date_made)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if recipe["name"] == "" or recipe["under30"] == "" or recipe["date_made"] == "" or recipe["description"] == "" or recipe["instructions"] == "":
            flash("All fields required.")
            is_valid = False
        if len(recipe['name']) < 3:
            flash("Name must be 3 characters long.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be 3 characters long.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be 3 characters long.")
            is_valid = False
        return is_valid

    @classmethod
    def update_one(cls,data):
        query = """
        UPDATE recipes SET 
        name = %(name)s,
        under30 = %(under30)s,
        date_made = %(date_made)s,
        description = %(description)s,
        instructions = %(instructions)s
        WHERE id=%(id)s;
        """
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        data = {"id":id}
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print (results)
        recipe = cls(results[0])
        user_data = {"id" : recipe.creator_id}
        recipe.user = user.User.get_by_id(user_data)
        return recipe
    
    @classmethod
    def show(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.creator_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        print (results)
        recipe = cls(results[0])
        recipe_data = {
                "id" : results[0]["users.id"],
                "name" : results[0]["name"],
                "under30" : results[0]["under30"],
                "date_made" : results[0]["date_made"],
                "description" : results[0]["description"],
                "instructions" : results[0]["instructions"]
            }
        recipe.user = user.User(recipe_data)
        return recipe