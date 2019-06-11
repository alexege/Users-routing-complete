from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

# /
@app.route("/")
def index():
    return render_template("index.html")

# /users/new-Get
@app.route("/users/new")
def new():
    return render_template("create.html")

# /users/create-POST
# Inserts the form data from create new user to the database
@app.route("/users/create", methods=["POST"])
def create():
    data = {
        "fname" : request.form['first_name'],
        "lname" : request.form['last_name'],
        "email" : request.form['email_name']
    }
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"
    db = connectToMySQL('restfulusers')
    user_id = db.query_db(query, data)
    return redirect("/users/" + str(user_id))

# /users/<id>-GET
@app.route("/users/<id>")
def display_user(id):
    data = {
        "id" : id
    }
    query = "SELECT * FROM users WHERE id = %(id)s"
    db = connectToMySQL('restfulusers')
    result = db.query_db(query, data)
    print("RESULT:")
    print(result)
    return render_template("show.html", result = result)

# /users-GET
@app.route("/users")
def display_all_users():
    query = "SELECT * FROM users"
    db = connectToMySQL("restfulusers")
    selection = db.query_db(query)
    return render_template("user_list.html", users=selection)
    # return render_template("user_list.html" users=selection)

# /users/<id>/edit-GET
@app.route("/users/<id>/edit")
def edit_user(id):
    data = {
        "id" : id
    }
    query = "SELECT * FROM users WHERE id = %(id)s"
    db = connectToMySQL("restfulusers")
    users = db.query_db(query, data)
    print("USERS: ")
    print(users)
    return render_template("edit_user.html", id=id, users=users)

# /users/<id>/update-POST
@app.route("/users/<id>/update", methods=["POST"])
def update_user(id):
    query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s WHERE id = %(id)s;"
    data = {
        'fname' : request.form['first_name'],
        'lname' : request.form['last_name'],
        'email' : request.form['email_name'],
        'id'    : id
    }
    db = connectToMySQL("restfulusers")
    users = db.query_db(query, data)
    print(users)
    return redirect("/users/" + str(id))

# /users/<id>/destroy-GET
@app.route("/users/<id>/destroy")
def destroy_user(id):
    data = {
        "id" : id
    }
    query = "DELETE FROM users WHERE id = %(id)s"
    db = connectToMySQL("restfulusers")
    db.query_db(query, data)
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)