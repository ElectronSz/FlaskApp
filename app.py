
from flask import Flask, render_template, request, redirect
from werkzeug import generate_password_hash, check_password_hash
from pymongo import MongoClient
import datetime
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.Api
users = db['user']

##***************=>Default Route**********************##
@app.route('/')
def index():
    return render_template('index.html')

##***************=>Users Route**********************##
@app.route("/users")
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


@app.route("/users/new")
def add_user_view():
    return render_template("add.html")


@app.route("/users/add", methods=["POST"])
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
            return redirect("/users")
        else:
            return "Error while adding user"
    except Exception as e:
        print(e)



@app.route("/users/edit/<id>")
def edit_view(id):
       user_out = db['user']
       row = user_out.find_one({"_id": ObjectId(id)})
       return render_template("edit.html", row=row)


@app.route("/users/update", methods=["POST"])
def update_user():
    try:
        _name = request.form["inputName"]
        _email = request.form["inputEmail"]
        _id = request.form["id"]
        # validate the received values
        if _name and _email and _id and request.method == "POST":
         
            #implement update
            user_out = db['user']
            user_out.update_one({'_id': ObjectId(_id)}, { "$set": { 'name': _name, 'email': _email } })
            return redirect("/users")
        else:
            return "Error while updating user"
    except Exception as e:
        print(e)


@app.route("/users/delete/<_id>")
def delete_user(_id):
    #implement delete
    user_out = db['user']
    user_out.delete_one({"_id": ObjectId(_id)})
    return redirect('/users')

##***************<=Users Route**********************##


##***************=>Houses Route**********************##
@app.route('/houses')
def houses():
    return render_template('houses.html')

@app.route("/houses/new")
def add_house_view():
    return render_template("add_house.html")