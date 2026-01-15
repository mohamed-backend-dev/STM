import sqlite3
import os
import time
db = sqlite3.connect("app.db")
cr = db.cursor()
cr.execute("create table if not exists users(user_id integer, name text unique)")
cr.execute("create table if not exists skills(user_id integer, skill text)")
def clear():
    """this function clear the terminal """
    time.sleep(3)
    os.system("cls" if os.name == "nt" else "clear")
def new_user():
    """this function add new user to the database"""
    name = input("inter your name : ")
      # loop للتاكد من الاسم غير مكرر
    cr.execute("select name from users")
    all_name = cr.fetchall()
    cr.execute("select count(user_id) from users")
    num_last_id = (cr.fetchone())[0]
    new_user_id = num_last_id + 1
    try:
        cr.execute(f"insert into users(user_id, name) values({new_user_id}, '{name}')")
        cr.execute(f"insert into skills(user_id) values({new_user_id})")
        print("user name added succesfuly")
    except sqlite3.IntegrityError :
        print("this name already taken ")
    db.commit()
def update_skill():
            """this function update the skill of the user in the database"""
            """to make sure the name is """
            os.system("cls" if os.name == "nt" else "clear")
            name = input("inter your name ")
            old_skill = input("inter the the old skill ")
            new_skill = input("inter the the new skill ")
            cr.execute(f"select users.user_id from users where users.name = '{name}' ")
            the_id = (cr.fetchone())[0]
            cr.execute(f"update skills set skill = '{new_skill}' where skill = '{old_skill}' ")
            print("skills updated succesfuly")
            db.commit()
def show_skill():
    """this function show all users with skills (not null)"""    
    cr.execute("select users.user_id, users.name, skills.skill from users join skills on users.user_id = skills.user_id")
    x = (cr.fetchall())
    for show in x :
        show_slice = show[0:2]
        if show[2] is not None :
            print(f"The name : {show_slice[1]} The id : {show_slice[0]}")
            print(f"skills : {show[2::1]}")
            print("_"*50)
        elif show[2] is None :
            continue
def append_skill():
    """this function append new skill to the users"""
    """to make sure the name is """
    os.system("cls" if os.name == "nt" else "clear")
    name = input("inter your name ")
    skill = input("inter the the skill ")
    cr.execute(f"select users.user_id from users where users.name = '{name}'")
    the_id = (cr.fetchone())[0]            
    cr.execute(f"insert into skills(user_id, skill) values({the_id}, '{skill}')")
    print("skills added succesfuly")
    db.commit()
def delete_skill():
    """this function delete skill or usesr from database"""
    name = input("inter your name ")
    skill = input("inter the the skill ")
    user_delete_choice = input("""what do you want to delete :
          1_ Delete a Skill
          2_ Delete your acount 
          your opptetion : """).lower()
    if user_delete_choice == "1" :
        cr.execute(f"delete from skills where skill = '{skill}'")
    db.commit()
    print("skill deleted")          
def quite_app():
    """this function close the code """
    db.close()
    clear()
    print("app closed")       
while True :
    user_choice = input("""what do you want to do today
"n" new user
"a" append a new skill
"s" show all skills 
"u" update a skill progress
"d" delete a skill 
"q" quite app  
inter an opption  """).lower()
    choices = ["n","a","s","u", "d", "q"]
    if user_choice in choices :
        if user_choice == "n":
            new_user()
            clear()
        elif user_choice == "a":
            append_skill()
            clear()
        elif user_choice == "s":
            show_skill()
            clear() 
        elif user_choice == "u":
            update_skill()
            clear()
        elif user_choice == "d":
            delete_skill()
            clear()
        elif user_choice == "q":
            quite_app()
            break
            

