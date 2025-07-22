from flask import Flask, render_template, request
from pymongo import MongoClient
from urllib.parse import quote_plus
app = Flask(__name__)

username = quote_plus("chandarohith10")
password = quote_plus("rohith10@2006")
client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.mvglpmf.mongodb.net/")
db = client["flaskdatabase"]
usercollection = db["user"]
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login")
def login():
    return render_template("form.html")
@app.route("/card")
def card():
    users = usercollection.find()
    # print(list(users))
    userdata=(list(users))
    return render_template("table.html", userdata=userdata)
    print(userdata)
@app.route("/greet",methods=["POST"])
def greet():
    name=request.form["username"]
    print(name)
    email=request.form["email"]
    print(email)
    password=request.form["password"]
    print(password)
    usercollection.insert_one({"username":name,"email":email,"password":password})
    return render_template("greet.html",username=name,email=email,password=password)
if __name__ == "__main__":
    app.run(debug=True)