from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post

# -----------------------Read one-------------------------------
@app.route("/dashboard")
def dashboard():
    # ***Login validation****
    if "user_id" not in session:
        return redirect("/") 
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", logged_in_user = User.get_by_id(data), all_the_posts= Post.get_all_posts_with_user()) 


# -- ------------------------- Create --------------------------->
@app.route("/submit_post", methods=["POST"])
def create_post():
    print(request.form)
    # logged in Validation
    if "user_id" not in session:
        return redirect("/") 
    # ----------------------- Validation ----------------------------
    if not Post.validate_post(request.form):
        return redirect("/dashboard")
    data = {
        "post": request.form['post'],
        "category" : request.form['category'],
        "user_id": session["user_id"]
    }
    Post.create_post(data)
    return redirect("/dashboard",)

#---------------------Delete post--------------------------------------
@app.route("/delete_post/<int:id>", methods=["POST"])
def delete_post(id):
    print(request.form)
    # logged in Validation
    if "user_id" not in session:
        return redirect("/") 
    data = {
        "id": id
    }
    Post.delete_post(data)
    return redirect("/dashboard")

# --------------------update------------------------------------------------
@app.route("/edit_post/<int:id>")
def edit_post(id):
    data = {
        "id": id
    }
    # call the query to get one animals from the get_one classmethod in the models folder 
    # We are using the same classmethod to get one animal as the read one route above
    an_animal = Animal.get_one(data) 
    return render_template("edit_animal.html", one_animal = an_animal)

@app.route("/update_post/<int:id>", methods = ["POST"])
def update_post(id):
    # ----------------------- Validation ----------------------------
    if not Post.validate_post(request.form):
        return redirect("/edit_post/{id}")
    data = {
        "id": id,
        "post": request.form["post"], 
        "category": request.form["category"]
    }
    Post.update_post(data)
    return redirect(f"/users_post/{id}")

