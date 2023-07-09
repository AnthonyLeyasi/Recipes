from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import flash

class Recipe:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = []

    @staticmethod
    def validate_recipe(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False
        if form_data['date_made'] == '':
            flash("Please input a date.")
            is_valid = False
        if 'under_30' not in form_data:
            flash("Give me cook time.")
            is_valid = False

        return is_valid




    @classmethod
    def get_one(cls, data):
        query = """
            SELECT * 
            FROM recipes 
            LEFT JOIN users ON recipes.user_id = users.id 
            WHERE recipes.id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return None
        recipe_data = result[0]
        recipe = cls(recipe_data)
        for row in result:
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            user = next((u for u in recipe.user if u.id == user_data['id']), None)
            if user is None:
                user = users.User(user_data)
                recipe.user.append(user)
        return recipe

    @classmethod
    def get_all(cls):
        query = """
            SELECT * 
            FROM recipes 
            LEFT JOIN users ON recipes.user_id = users.id;
        """
        result = connectToMySQL(cls.DB).query_db(query)
        if not result:
            return None
        recipe_data = []
        for row in result:
            recipe = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            # user = next((u for u in recipe.user if u.id == user_data['id']), None)
            # if user is None:
            recipe.user = users.User(user_data)
            recipe_data.append(recipe)
        return recipe_data



    @classmethod
    def save(cls,form_data):
        query = """
                INSERT INTO recipes (name,description,instructions,date_made,under_30,user_id)
                VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s,%(user_id)s);
                """
        return connectToMySQL(cls.DB).query_db(query,form_data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """
        result = connectToMySQL(cls.DB).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_recipe = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_recipe.creator = users.User(user_data)
        return this_recipe

    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE recipes
                SET name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s ,
                date_made = %(date_made)s,
                under_30 = %(under_30)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.DB).query_db(query,form_data)