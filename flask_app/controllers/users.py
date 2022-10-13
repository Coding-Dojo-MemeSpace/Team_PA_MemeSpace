from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def groot():
    return render_template("home_page.html")

#-- -------------------------Registration --------------------------
@app.route("/create_user", methods=["POST"])
def create_user():
    # print(request.form)
    # --------------------validation -----------------------------------
    if not User.validate_create(request.form):
        return redirect("/") #redirect back to the create form
    # -------------(Bcrypt) Hash password after validation but before data dictionary-----------
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # print(pw_hash)
    data ={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
        #we do not need password Conf because we only need to store the password once
    }
    user_id = User.create(data) 
    session["user_id"] = user_id 
    return redirect("/dashboard") 


# --------------------Login -----------------------------
@app.route("/login", methods =["POST"])
def login():
    # print(request.form)
    # see if the user's email provided exists in the database 
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data) 
    # user is not registered in the db, they will get the flash message and redirected
    if not user_in_db:
        flash("Invalid Email/Password", "login") #"login" is the validation catagory filter
        return redirect("/")
        #this is to check that the email and password are in the same row in the database table
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password, we flash message and redirect
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")




    # ------------------Logout ----------------- --
@app.route("/logout")
def logout():
    # This line will get rid of everything stored in session 
    session.clear()
    return redirect("/")

