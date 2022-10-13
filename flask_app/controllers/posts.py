from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post

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
    Post.create(data)
    return redirect("/dashboard")

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
    Post.delete(data)
    return redirect("/dashboard")


