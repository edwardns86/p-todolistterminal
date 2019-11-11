import os
import sqlite3
import sys
import datetime
from termcolor import colored
from tabulate import tabulate


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor() 
Status = True

user = ""

sql = """
CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date DATE DEFAULT "todaydatetime.datetime.now()",
    status TEXT DEFAULT "incomplete",
    priority INTEGER DEFAULT "5",
    hours_needed INTEGER ,
    user_id INTEGER 
    )
"""
cur.execute(sql)
conn.commit()

sql = """
CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY,
    project name TEXT NOT NULL
    )
"""
cur.execute(sql)
conn.commit()

sql = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
    )
"""
cur.execute(sql)
conn.commit()

def login():
    
    print("Enter your email.")
    email = input()

    sql = """
    SELECT * FROM users
    WHERE email = ?
    
    """
    cur.execute(sql,(email,))
    results = cur.fetchall()

    if len(results) > 0:
        
        return results[0]
    else:
        sql = """
        INSERT INTO users(
            name, 
            email
        ) 
        VALUES (?,?)
        """

        print("Enter your name.")
        name = input()
        cur.execute(sql,(name, email))
        conn.commit()
        sql = """
            SELECT * FROM users
            WHERE email = ?
        """
        cur.execute(sql,(email,))
        results = cur.fetchall()
        return results[0]

def delete_user():
    sql = """ 
    DELETE FROM users 
    WHERE id = ?
    ;
    """ 
    show_users()
    print("what user id do you want to permenantly delete?") 
    edit_id = input()

    cur.execute(sql,(edit_id,))
    conn.commit()
    show_users()

def show_users():
    sql = """
    SELECT * FROM users
    """    
    cur.execute(sql)
    results = cur.fetchall()
    print("Here are all the current users")
    print (colored(tabulate(results, headers=['ID', 'Name', 'Email' ], tablefmt='fancy_grid'), "blue"))    

def list(user):
    sql = """
        SELECT * FROM todos
        WHERE status NOT LIKE "Trash"
        AND user_id = ?
    """
    user_id = user[0]

    cur.execute(sql,(user_id,))
    results = cur.fetchall()
    print ("Here are all your tasks " + user[1])
    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed', 'User ID' ], tablefmt='fancy_grid'), "green"))

def masterlist():
    sql = """
        SELECT * FROM todos
    """
    cur.execute(sql)
    results = cur.fetchall()

    print("The complete todos table")
    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed' , 'User ID' ], tablefmt='fancy_grid'), "green"))

def add(user):
    sql = """
        INSERT INTO todos(
        body, 
        due_date,
        priority,
        hours_needed,
        user_id
    ) VALUES (?,?,?,?,?)
    """
    print("name your task")
    taskname = input()

    print("when does it need to be completed by?")
    date = input()

    print("give the task a priority from 1 to 10")
    priority_score = input()

    print("how long in hours will it take?")
    hours = input()

    user_id = user[0]

    cur.execute(sql,(taskname, date , priority_score, hours, user_id))
    conn.commit()

    print (colored("Here is your new task " + user[1],"blue"))
    sql = """
    SELECT * FROM todos
    ORDER BY id DESC
    LIMIT 1 ; 
    """
    cur.execute(sql)
    results = cur.fetchall()

    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed' , 'User ID'], tablefmt='fancy_grid'), "green"))

def delete(user):
    sql = """ 
    DELETE FROM todos 
    WHERE id = ?
        AND status LIKE "Trash"
    ;
    """ 
    show_trash_bin(user)
    print("what task id do you want to permenantly delete?") 
    edit_id = input()

    cur.execute(sql,(edit_id))
    conn.commit()
    

def edit(user):

    sql = """
    UPDATE todos
    SET body = ? , 
        due_date = ?,
        status = ?,
        priority = ?,
        hours_needed = ?

    WHERE id = ?
    AND user_id = ?
    ; 
    """

    print("Here are your tasks")
    list(user)
    print("What task ID do you want to edit?")
    edit_id = input()
        # Check if task id exists 
    print("Edit the task name")
    edit_body = input()
    print("Edit when the task is due")
    edit_due = input()
    print("Edit the current status")
    edit_status = input()
    print ("Edit the priority")
    edit_priority = input()
    print ("Edit how many hours it will take")
    edit_hours = input()

    user_id = user[0]

    cur.execute(sql,( edit_body , edit_due, edit_status, edit_priority, edit_hours, edit_id, user_id))
    conn.commit()

    list(user)

# This function marks a task as completed
def complete(user):
    sql = """
    UPDATE todos
    SET status = "Complete"    
    WHERE id = ?
    AND user_id = ?
    ; 
    """
    print("Here are your tasks")
    list(user)
    print("What task ID do you want to mark completed?")
    edit_id = input()
    user_id = user[0]
    cur.execute(sql,(edit_id, user_id))
    conn.commit()


def show_incomplete(user):
    sql = """
        SELECT * FROM todos
        WHERE status NOT LIKE "complete"
            AND status NOT LIKE "trash"
            AND user_id =? ;
    """ 
    user_id = user[0]
    cur.execute(sql, (user_id,))
    results = cur.fetchall()
    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed', 'User ID' ], tablefmt='fancy_grid'), "green"))


def show_complete(user):
    sql = """
        SELECT * FROM todos
        WHERE status LIKE "complete"
        AND status NOT LIKE "trash"
        AND user_id = ?;
    """ 
    user_id = user[0]
    cur.execute(sql, (user_id,))
    results = cur.fetchall()
    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed' , 'User ID'], tablefmt='fancy_grid'), "green"))


def show_quick(user):
    sql = """
        SELECT * FROM todos
        WHERE hours_needed < 2 
        AND status NOT LIKE "complete"
        AND status NOT LIKE "trash"
        AND user_id = ?;
    """ 
    user_id = user[0]
    cur.execute(sql, (user_id,))
    results = cur.fetchall()
    print("Here are some quick tasks for you to do")
    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed' , 'User ID' ], tablefmt='fancy_grid'), "green"))


def show_important(user):
    sql = """
        SELECT * FROM todos
        WHERE priority >= 5 
            AND status NOT LIKE "complete"
            AND status NOT LIKE "trash"
            AND user_id = ?
        ORDER BY priority DESC
        LIMIT 5
        ;
    """ 

    user_id = user[0]
    cur.execute(sql, (user_id,))
    results = cur.fetchall()
    print("These are your most important tasks at the moment")
    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed' , 'User ID' ], tablefmt='fancy_grid'), "green"))


def show_help_menu():
    print (colored(tabulate([
    ['add', '+' ,colored('Creates a new task', "red")],
    ['edit', 'e' ,'Edits an existing task'],
    ['complete', 'c','Marks a task completed'],
    ['list', 'l' ,'Shows all tasks'],
    ['show_incomplete', 'si','Shows all tasks that need to be completed'],
    ['show_complete', 'sc','Shows all completed tasks'],
    ['show_quick', 'sq','Shows all tasks that will take an hour or less'],
    ['show_important','sim' ,'Shows the 5 tasks with the highest priority score'],
    ['show_trash', 'st' ,'Shows all tasks in the trash bin'],
    ['trash', 't' ,'Puts a task in the trash bin'],
    ['restore', 'r' ,'Moves a task from the trash bin back to the main list'],
    ['delete', '-' ,'Delete a task from trash bin'],
    ['list', 'l' ,'Shows all tasks that are not in trash'],
    ['help', 'h' ,'Shows all available commands'],
    ['master_list', 'ml', 'Shows a full copy of the tasks'],
    ['close', '' ,'Logs out of ED TASK']
    ], 
    headers=['Command', 'Shortcut Key','Result' ], tablefmt='fancy_grid'), "green"))


# This functions puts something in trash
def bin(user): 
    sql = """
    UPDATE todos
    SET status = "Trash"    
    WHERE id = ?
    AND user_id = ?; 
    """
    print("Here are your tasks")
    list(user)
    print("What task ID do you want to move to trash?")
    edit_id = input()
    user_id = user[0]
    cur.execute(sql,(edit_id, user_id))
    conn.commit()
    show_trash_bin(user)

# This function deletes something from trash 


# Puts it back in main list
def restore(user):
    sql = """
    UPDATE todos
    SET status = "incomplete"    
    WHERE id = ?
    AND user_id = ?
    ; 
    """

    show_trash_bin(user)
    print("What task ID do you want restore?")
    edit_id = input()
    user_id = user[0]
    cur.execute(sql,(edit_id, user_id))
    conn.commit()

#Shows trash bin 
def show_trash_bin(user):
    sql = """
    SELECT * FROM todos
    WHERE status LIKE "Trash"
    AND user_id = ?
    ; 
    """
    user_id = user[0]
    cur.execute(sql, (user_id,))
    results = cur.fetchall()
    print("Here is the current trash bin")
    print (colored(tabulate(results, headers=['ID', 'Task', 'Due Date' , 'Current Status' , 'Priority' , 'Hours Needed', 'User ID' ], tablefmt='fancy_grid'), "green"))

def close(user):
    print("Goodbye " + user[1])
    print (colored("""
    ____ ____ _________ ____ ____ ____ ____ 
    ||E |||D |||       |||T |||A |||S |||K ||
    ||__|||__|||_______|||__|||__|||__|||__||
    |/__\|/__\|/_______\|/__\|/__\|/__\|/__\|
    """, "red"))
    sys.exit()

def handle_choices(user):
    choice = input()
    if choice == "list" or choice == "l":
                list(user)
    elif choice == "add" or  choice == "+":
                add(user)
    elif choice == "delete" or choice == "-":
                delete(user)
    elif choice == "edit" or choice ==  "e":
                edit(user)
    elif choice == "complete" or choice == "c":
                complete(user)
    elif choice == "show_incomplete" or choice == "si" :
            show_incomplete(user)
    elif choice == "show_complete" or choice == "sc":
            show_complete(user)
    elif choice == "show_quick" or choice == "sq":
            show_quick(user)
    elif choice == "show_important" or choice == "sim":
            show_important(user)
    elif choice == "trash" or choice == "t":
            bin(user)
    elif choice == "show_trash" or choice == "st":
            show_trash_bin(user) 
    elif choice == "restore" or choice == "r":
            restore(user)               
    elif choice == "help" or choice == "h":
            show_help_menu()
    elif choice == "master_list" or choice == "ml":
            masterlist()
    elif choice == "show_users" or choice == "su":
            show_users()  
    elif choice == "delete_user" or choice == "du":
            delete_user()      
    elif choice == 'close':
            close(user)
    else: 
        print("Incorrect command check out the options below...")  
        show_help_menu()

if __name__  == '__main__':
    print (colored("""
    ____ ____ _________ ____ ____ ____ ____ 
    ||E |||D |||       |||T |||A |||S |||K ||
    ||__|||__|||_______|||__|||__|||__|||__||
    |/__\|/__\|/_______\|/__\|/__\|/__\|/__\|
    """, "green"))
    print("Nice to meet you, my name is Ed I am a task manager.")
    print("I can help you manage everything you have to do.")
    print("Before I start working I need you to login")
    user = login()
    while Status:
        # try:
            print (colored("Hi " + user[1], "blue"))
            print(colored("Type help below to see a list of available commands if you haven't used the tool before.", "blue"))
            print(colored("So, what do you want to do?", "blue"))
            handle_choices(user)
            
        # except:
            # print (colored("Error!", "red"))