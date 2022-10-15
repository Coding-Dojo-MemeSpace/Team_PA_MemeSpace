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
        self.users_who_like = []
        self.ids_who_like = []

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

#----------------------many-to-many relationship----------------------
    @classmethod
    def get_all_info(cls):
        query = '''
        SELECT * FROM posts JOIN users AS posters ON posts.user_id = posters.id
        LEFT JOIN likes ON posts.id = likes.post_id
        LEFT JOIN users AS likers on likers.id = likes.user_id ORDER BY likes.post_id ASC;
        '''
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_posts = []

        for row in results:
            if len(all_posts) == 0 or all_posts[len(all_posts) -1].id != row['id']:
                one_post = cls(row)
                user_data = {
                    "id": row['posters.id'], 
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['posters.created_at'],
                    "updated_at": row['posters.updated_at']
                }
                user_obj = user.User(user_data)
                one_post.poster = user_obj
                if row['likers.id'] != None:
                    liker_data = {
                        "id": row['likers.id'], 
                        "first_name": row['likers.first_name'],
                        "last_name": row['likers.last_name'],
                        "email": row['likers.email'],
                        "password": row['likers.password'],
                        "created_at": row['likers.created_at'],
                        "updated_at": row['likers.updated_at']
                    }
                    liker_obj = user.User(liker_data)
                    one_post.users_who_like.append(liker_obj) ##Need to figure out where the varabile  users_who_like came from. 53.23
                    one_post.ids_who_like.append(liker_obj)
                all_posts.append(one_post)
            else:
                liker_data = {
                    "id": row['likers.id'], 
                    "first_name": row['likers.first_name'],
                    "last_name": row['likers.last_name'],
                    "email": row['likers.email'],
                    "password": row['likers.password'],
                    "created_at": row['likers.created_at'],
                    "updated_at": row['likers.updated_at']
                }
                liker_obj = user.User(liker_data)
                all_posts[len(all_posts)-1].users_who_like.append(liker_obj)
                all_posts[len(all_posts)-1].ids_who_like.append(liker_obj.id)
        return all_posts

        

#-----------------------Like Post----------------------------
    @classmethod
    def like(cls, data):
        query = "INSERT into likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data) 
        print(results)
        return results

#-----------------------unlike Post----------------------------
    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data) 
        print(results)
        return results

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
