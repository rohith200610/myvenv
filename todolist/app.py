from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)

client=MongoClient("mongodb+srv://chandarohith10:rohith10@cluster0.mvglpmf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
print('client:',client)
db=client["taskcollection"]
task_collection=db["tasks"]
tasks_storage = []

@app.route("/")
def home():
    return redirect(url_for('index'))


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/task")
def task():
    return render_template("task.html")

@app.route("/addtask", methods=["POST"])
def addtask():
    task_name = request.form["task_name"]
    task_description = request.form.get("task_description", "")
    task_priority = request.form.get("priority", "medium")
    task_status = request.form.get("status", "pending") 
    
    print(f"Task Name: {task_name}") 
    print(f"Description: {task_description}") 
    print(f"Priority: {task_priority}") 
    print(f"Status: {task_status}") 
    
    
    task_data = {
        "name": task_name,
        "description": task_description,
        "priority": task_priority,
        "status": task_status
    }
    
    task_collection.insert_one({"task_name":task_name,"task_description":task_description,"priority":task_priority,"status":task_status})
    return render_template("task.html", 
                         task_name=task_name,
                         task_description=task_description,
                         priority=task_priority,
                         status=task_status)

@app.route("/all_tasks")
def all_tasks():
    tasks = task_collection.find()
    taskdata  =(list(tasks))
    return render_template("all_tasks.html", taskdata=taskdata)





@app.route("/edit/<id>")
def edit(id):
    task = task_collection.find_one({"_id": ObjectId(id)})
    print(task)
    return render_template("edit.html", task=task)

@app.route("/update/<id>", methods=["POST"])
def update(id):
    task_name = request.form["task_name"]
    task_description=request.form.get("task_description", "")
    task_priority=request.form.get("priority")
    task_status=request.form.get("status")

    task_collection.update_one({"_id": ObjectId(id)},{"$set": {"task_name":task_name,"task_description":task_description,"priority":task_priority,"status":task_status}})
    return "ok"


@app.route("/delete/<id>")
def delete(id):
    task_collection.delete_one({"_id": ObjectId(id)})
    return redirect("/all_tasks")

if __name__ == "__main__":
    app.run(debug=True)

