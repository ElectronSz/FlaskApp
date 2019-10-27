
from flask import Flask, render_template, request, redirect
from werkzeug import generate_password_hash, check_password_hash
from pymongo import MongoClient
import datetime

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.Api
users = db['user']


@app.route("/new_user")
def add_user_view():
    return render_template("add.html")


@app.route("/add", methods=["POST"])
def add_user():
    try:
        _name = request.form["inputName"]
        _email = request.form["inputEmail"]
        _password = request.form["inputPassword"]
        # validate the received values
        if _name and _email and _password and request.method == "POST":
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            user_in = db['user']
            user = {
                'name': _name,
                'email': _email,
                'password': _hashed_password,
                'date_reg': datetime.datetime.utcnow()
            }

            user_in.insert_one(user)
            return redirect("/")
        else:
            return "Error while adding user"
    except Exception as e:
        print(e)


@app.route("/")
def users():
    try:
        user_arr = list()
        user_out = db['user']
        user_list = user_out.find()
        for user in user_list:
            user_arr.append(user)
        return render_template("users.html", table=user_arr)
    except Exception as e:
        print(e)


@app.route("/edit/<int:id>")
def edit_view(id):
    try:
       
       return render_template("edit.html")
    except Exception as e:
        print(e)


@app.route("/update", methods=["POST"])
def update_user():
    try:
        _name = request.form["inputName"]
        _email = request.form["inputEmail"]
        _password = request.form["inputPassword"]
        _id = request.form["id"]
        # validate the received values
        if _name and _email and _password and _id and request.method == "POST":
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)

           #implement update

            return redirect("/")
        else:
            return "Error while updating user"
    except Exception as e:
        print(e)


@app.route("/delete/<int:id>")
def delete_user(id):
    try:
        #implement delete

        return redirect("/")
    except Exception as e:
        print(e)
