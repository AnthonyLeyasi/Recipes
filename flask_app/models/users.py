from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipes
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "recipes"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email ,password ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.DB).query_db(query, user)
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name should be at least 2 characters.")
            is_valid = False

        if len(user['last_name']) < 2:
            flash("Last name should be at least 3 characters.")
            is_valid = False

        if len(user['email']) == 0:
            flash("Email is required.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format.")
            is_valid = False
        if len(result) >= 1:
            flash("Email already in use.")
            is_valid = False
        
        if len(user['password']) == 0:
            flash("Password is required.")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password should be at least 8 characters.")
            is_valid = False

        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])