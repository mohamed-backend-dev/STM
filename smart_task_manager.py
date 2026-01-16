from flask import Flask , render_template , request, redirect, url_for, session
import sqlite3
import datetime
import os
# make the data base
import os
import sqlite3

db_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_dir, "data_base")

# إنشاء الفولدر إذا لم يكن موجودًا
os.makedirs(db_path, exist_ok=True)

# 
task_db = os.path.join(db_path, "task.db") 


def make_the_data_base():
   db = sqlite3.connect(task_db)
   cr = db.cursor()
   cr.execute("create table if not exists users( user_password integer unique, user_email text unique, user_name text unique)")
   cr.execute("create table if not exists tasks( user_password integer , user_tasks text, time text)")
   db.commit()
   db.close()
make_the_data_base()
# end of making data base
# ________________________
# flask
smart_task_manager = Flask(__name__)
smart_task_manager.secret_key = os.environ.get("SECRET_KEY")
# login page
@smart_task_manager.route("/", methods = ["GET","POST"] )
def login():
    session.clear()
    wrong = None
    if request.method =="POST":
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        db = sqlite3.connect(task_db)
        cr = db.cursor()
        cr.execute("select * from users where user_password = ? and user_name = ? ",(user_password, user_name))
        result = cr.fetchone()
        if result == None :
            wrong = "0"
            db.close()
        else:
            wrong = None
            session["user_password"] = user_password
            db.close()
            return redirect(url_for('show_page'))
    return render_template("login.html", wrong = wrong)
# new user page
@smart_task_manager.route("/new_user", methods = ["GET","POST"])
def new_user():
    wrong = None
    yes = None
    if request.method == "POST":
        new_user_name = request.form["new_user_name"]
        new_user_email = request.form["new_user_email"]
        new_user_password = request.form["new_user_password"]
        db = sqlite3.connect(task_db)
        cr = db.cursor()
        cr.execute("select user_password from users where user_name = ? or user_email = ?",(new_user_name, new_user_email))
        result = cr.fetchone()
        if result == None :
            wrong = None
            yes = "0"
            cr.execute(f"insert into users(user_password, user_name, user_email) values({new_user_password}, '{new_user_name}', '{new_user_email}')")
            db.commit()
            db.close()
        else:
            wrong = '0'
            yes = None
            db.close()
    return render_template("new_user.html", wrong = wrong, yes = yes)
@smart_task_manager.route("/show", methods = ["GET", "POST"])
def show_page():
    if "user_password" not in session :
        return redirect("/")
    sure = None 
    user_password =session["user_password"]
    if request.method == "POST":
        add = request.form["add"]
        new_update = request.form["new_update"]
        old_update = request.form["old_update"]
        delete = request.form["delete"]
        sure = "yes in post if"
        if add :
            date = datetime.datetime.now()
            time = date.strftime("%Y-%m-%d")
            sure = "yes"
            db = sqlite3.connect(task_db)
            cr = db.cursor()
            cr.execute(f"insert into tasks(user_password, user_tasks, time) values ({user_password}, '{add}', '{time}')")
            db.commit()
        if new_update and old_update :
            db = sqlite3.connect(task_db)
            cr = db.cursor()
            cr.execute(f"update tasks set user_tasks = '{new_update}' where user_tasks = '{old_update}'")
            db.commit()
        if delete :
            db = sqlite3.connect(task_db)
            cr = db.cursor()
            cr.execute(f"delete from tasks where user_tasks = '{delete}'")
            db.commit()
    return render_template("show.html", sure = sure)
@smart_task_manager.route("/display")
def display():
    if "user_password" not in session :
        return redirect("/")
    user_password = session["user_password"]
    db = sqlite3.connect(task_db)
    cr = db.cursor()
    cr.execute(f"select user_tasks, time from tasks where user_password = {user_password}")
    all_tasks = cr.fetchall()
    db.commit()
    return render_template("display.html", all_tasks = all_tasks)
if __name__ == "__main__":
    smart_task_manager.run()
    #first commit
    #new commit
    #who is my code
