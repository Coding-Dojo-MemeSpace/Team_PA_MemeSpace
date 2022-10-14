from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import post
import re   # the regex module
# create a regular expression object that we'll use later (validation)   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX =re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z\d]+$")
# At least one upper case English letter, (?=.*[A-Z])
# At least one lower case English letter, (?=.*[a-z])
# At least one digit, (?=.*[0-9])


class User:

    db = "memespace"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.post = []

#-- -------------------------Registration (Create User) --------------------------
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results


# --------------------Login --------------------------------------
    @classmethod
    def get_by_email (cls, data): 
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data) 
        print(results)
        # this if statement is for the validating if the email already exist in the database
        if results == (): #when we pass in an email not inside the database it returns an empty tuple ()
            return False
        # otherwise we are creating an users instance 
        return (cls(results[0])) #we are returning the users instance to the controller route



# ------------------------Read one -------------------------------
    @classmethod
    def get_by_id (cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        # we are creating an users instance
        return (cls(results[0])) #we are returning the users instance to the controller route



# -----------------------Read one to JOIN Users and Post-------------------------------
    @classmethod
    def get_one_with_post(cls, data): 
        query = "SELECT * FROM users JOIN posts ON users.id = posts.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data) 
        print(results)
        one_user = cls(results[0])
        for one_post in results:
            post_data = {
                "id" : one_post["posts.id"], 
                "post" :one_post["post"],
                "category" : one_post["category"],
                "created_at": one_post["posts.created_at"],
                "updated_at": one_post["posts.updated_at"]
            }
            post_obj = post.Post(post_data) 
            one_user.post.append(post_obj)
        return one_user


# --------------------validation -----------------------------------
    @staticmethod
    def validate_create(user): #user is the request.form information that we are passing in
        is_valid = True
        if len(user["first_name"]) <2:
            flash("First name is too short!", "create_user") #"create_user" is the validation catagory filter
            is_valid = False
        if len(user["last_name"]) <2:
            flash("last name is too short!", "create_user")
            is_valid = False
        if len(user["email"]) <6:
            flash("Email is too short!", "create_user")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address format!", "create_user")
            is_valid = False
        if len(user["password"]) <8:
            flash("Password is too short!", "create_user")
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Invalid password format! Need 1 uppercase letter and 1 number", "create_user")
            is_valid = False
        #if the value of password does not equal to the password conf
        if user["password"] != user["password_conf"]: 
            flash("Password do not match!", "create_user")
            is_valid = False
        # If the email is already in database (this requires a query to check if the email is in the database)
        data = {
            "email" : user["email"]
        }
        user_in_db = User.get_by_email(data) 
        if user_in_db:
            flash("Email already taken.", "create_user")
            is_valid = False
        return is_valid
