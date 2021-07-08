# Programme Topic: Complete Flask Tutorial by CodeWithHarry

from flask import Flask # Importing the Flask class from the flask module
from flask import render_template # Importing render_template function to render .html templates
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_talisman import Talisman

app = Flask(__name__, static_folder="Static", template_folder="Templates") # Creating a Flask app
# Talisman(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(600), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Creating a route to make a page
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
    # print(allTodo)
    return render_template("index.html", allTodo=allTodo)

# Creating another route to make another page
@app.route("/about")
def about():
    return render_template('about.html')
    # return "This is the about page!" # This text is displayed in the webpage

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)

# Static and Template Directories

# Static Folder: This contains types of files which we want to be served directely into our website. Ex: .png, .txt, .py
# Templates Folder: The folder contains our template files which we want to render into our website. Ex: .html, .css, .js
