from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/auth_db"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User Model
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data["_id"]
        self.username = user_data["username"]

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": user_id})
    return User(user_data) if user_data else None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = mongo.db.users.find_one({"username": username})

        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for("profile"))

    return render_template("login.html")

@app.route("/profile")
@login_required
def profile():
    return f"Welcome, {current_user.username}!"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)