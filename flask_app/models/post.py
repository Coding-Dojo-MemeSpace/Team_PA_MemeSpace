from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Post:

    db = "memespace"

    def __init__(self, data):
        self.id = data["id"]
        self.post = data["post"]
        self.category = data["category"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.user_id = data["user_id"]
        self.poster = None

# -- ------------------------- Create --------------------------->
    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (post,category, user_id) VALUES (%(post)s, %(category)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results 

#---------------------Delete --------------------------------------
    @classmethod
    def delete_post(cls, data): 
        query = "DELETE FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results

# ----------------------------Update---------------------------------------------
    @classmethod
    def update_post(cls, data):
        query = "UPDATE posts SET post = %(post)s, category = %(category)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results


# *****Associating Users in Classes*******
# classmethod that will get all posts, and their one associated User that posted it
    @classmethod
    def get_all_posts_with_user(cls):
        # The MANY goes on the left hand side of the JOIN while the ONE goes on the right side of the JOIN
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        # We have an empty list to hold all the post instances that have the user instance inside of them
        all_posts = []
        for row in results:
            one_post = cls(row)
            user_data = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_post.poster = user_obj
            all_posts.append(one_post)
        return all_posts



# ---------------------Read one -----------------------
    @classmethod
    def get_one_with_user(cls, data): 
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data) 
        print(results)
        post = cls(results[0])
        user_data = {
            # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
            "id": results[0]['users.id'], 
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }
        user_obj = user.User(user_data)
        # Associate the Recipe class instance with the User class instance by filling in the empty chef attribute in the Recipe class (self.chef = None)
        post.poster = user_obj
        return post

# --------------------validation -----------------------------------
    @staticmethod
    def validate_post(post): #post is the form information that we are passing in
        is_valid = True
        if len(post["post"]) <5:
            flash("Post is too short!")
            is_valid = False
        return is_valid

#need validation for category