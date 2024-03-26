import sqlite3
import datetime


def create_table():
    with sqlite3.connect('Task.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Task ( 
                id INTEGER PRIMARY KEY, 
                table_name TEXT, 
                table_description TEXT,
                datetime_create DATETIME,
                date_deadline DATETIME
            ) 
        ''')


def add_task(conn) -> None:
    cursor = conn.cursor()
    name = input("Input task name: ")
    description = input("Write about the task: ")
    create_date = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
    deadline = input("Write deadline date in format YYYY-MM-DD: ")
    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("INSERT INTO Task(table_name, table_description, datetime_create, date_deadline)"
                       " VALUES (?,?,?,?)", (name, description, create_date, deadline))
        conn.commit()
        print("Task was added")
    except (ValueError, TypeError):
        print("Invalid date")


def change_task(conn) -> None:
    cursor = conn.cursor()
    name = input("Input the name of the task to be changed: ")
    task = cursor.execute("SELECT * FROM Task WHERE table_name = ?", (name,)).fetchone()
    if task:
        new_name = input("Input new task name: ")
        new_description = input("Write new description: ")
        new_deadline = input("Write new deadline date in format YYYY-MM-DD: ")
        create_date = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
        new_deadline = datetime.datetime.strptime(new_deadline, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE Task SET "
                       "table_name = ?, "
                       "table_description = ?, "
                       "datetime_create = ?, "
                       "date_deadline = ? "
                       "WHERE table_name = ?", (new_name, new_description, create_date, new_deadline, name,))
    else:
        print(f"Task with name {name} has no exists")


def view_all_tasks(conn) -> list:
    cursor = conn.cursor()
    select_request = """SELECT * FROM Task"""
    cursor.execute(select_request)
    res = cursor.fetchall()
    return res


def view_one_task(conn) -> tuple:
    cursor = conn.cursor()
    name = input("Input the name of the task to look: ")
    try:
        res = cursor.execute("SELECT * FROM Task WHERE table_name = ?", (name,)).fetchone()
        return res
    except (ValueError, TypeError):
        print("Name error")
        exit()


def delete_task(conn) -> None:
    cursor = conn.cursor()
    name = input("Input the name of the task to be deleted: ")
    if cursor.execute("SELECT * FROM Task WHERE table_name = ?", (name,)).fetchone():
        cursor.execute("DELETE FROM Task WHERE table_name = ?", (name,))
        conn.commit()
    else:
        print(f"Task with name {name} has no exists")


def print_hi(name):
    print(f'Hi, {name}')


def print_list(tasks) -> None:
    for i in tasks:
        print(i)


def menu():
    with sqlite3.connect('Task.sqlite') as conn:

        flag = True
        while flag:
            print("1 - add task\n2 - change task\n3 - view all tasks\n4 - view one task\n5 - delete task\n0 - exit")
            num = int(input(">> "))
            match num:
                case 1:
                    add_task(conn)
                case 2:
                    change_task(conn)
                case 3:
                    tasks = view_all_tasks(conn)
                    print_list(tasks)
                case 4:
                    task = view_one_task(conn)
                    print_list(task)
                case 5:
                    delete_task(conn)
                case 0:
                    flag = False
                case _:
                    print("This command is no exists!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('User')
    create_table()
#    insert_data()
    menu()
