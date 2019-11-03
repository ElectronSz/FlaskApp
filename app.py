
from flask import Flask, render_template, request, redirect
from werkzeug import generate_password_hash, check_password_hash
from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId
from rethinkdb import RethinkDB
r = RethinkDB()

app = Flask(__name__)
UPLOAD_FOLDER =os.getcwd()+"/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('mongodb+srv://mongodb:mongo1828@cluster0-iogp2.gcp.mongodb.net/house?retryWrites=true&w=majority')
db = client.Api
users = db['user']

#rethinkd config
conn = r.connect('localhost', 28015).repl()

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


@app.route("/charts")
def charts():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('charts.html', values=values, labels=labels, legend=legend)

@app.route("/rethink")
def rethink():
    cursor = r.db('Api').table("users").run(conn)
    users = []
    for user in cursor:
        users.append(user)
    
    return render_template('rethink.html',users=users)

@app.route("/rethink/new")
def add_rethink_view():
    return render_template("user_add.html")



@app.route("/rethink/add", methods=["POST"])
def rethink_user():
    try:
        _name = request.form["fullname"]
        _email = request.form["email"]
        _phone = request.form["phone"]
        _avatar = request.files["avatar"]
        # validate the received values
        if _name and _email and _phone and request.method == "POST":
            
            _avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], _avatar.filename))

            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'])+"/"+_avatar.filename
            fh = open(avatar_path, 'rb')
            contents = fh.read()
            fh.close()

            user = {
                'name': _name,
                'email': _email,
                'phone': _phone,
                'avatar_bn': r.binary(contents),
                'avatar_img': _avatar.filename,
                'timestamp': r.expr(datetime.now(r.make_timezone('+02:00')))
            }

           
            r.db('Api').table("users").insert(
                [
                    user
                ]
            ).run(conn)

            return redirect("/rethink")
        else:
            return "Error while adding user"
    except Exception as e:
        print(e)


@app.route("/rethink/edit/<id>")
def rethink_edit_view(id):
    row = r.db('Api').table('users').get(id).run(conn)
    return render_template("rethink_edit.html", row=row)


@app.route("/rethink/update", methods=["POST"])
def rethink_update_user():
    try:
        _name = request.form["name"]
        _email = request.form["email"]
        _phone = request.form["phone"]
        _id = request.form["id"]
        # validate the received values
        if _name and _email and _id and _phone and request.method == "POST":
         
            #update
            r.db('Api').table("users").filter(r.row['id'] == _id).update({"name": _name, "email": _email, "phone": _phone}).run(conn)
            return redirect("/rethink")
        else:
            return "Error while updating user"
    except Exception as e:
        print(e)



@app.route("/rethink/delete/<id>")
def rethink_delete_user(id):
    #implement delete
    r.db('Api').table("users").filter(r.row['id'] == id).delete().run(conn)
    return redirect('/rethink')