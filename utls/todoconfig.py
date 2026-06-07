import sqlite3

DB_NAME="todoconfig.db"


def get_connected():
    return sqlite3.connect(DB_NAME)

def init_table():

    con=get_connected()
    cursor=con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS todo(task_id INTEGER PRIMARY KEY AUTOINCREMENT, member_id INT NOT NULL, task_text TEXT NOT NULL)")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_member ON todo(member_id)") # This add a pointing index to the member_id for better searching 

    con.commit()
    cursor.close()

def add_task(member_id:int,task_text:str):

    con=get_connected()
    cursor=con.cursor()

    query="INSERT INTO todo(member_id,task_text) VALUES(?,?)"
    cursor.execute(query,(member_id,task_text))

    new_id=cursor.lastrowid # get id of newest inserted row

    con.commit()
    cursor.close()

    return new_id

def view_task(member_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT task_id, task_text FROM todo WHERE member_id=? ORDER BY task_id ASC"

    cursor.execute(query,(member_id,))

    rows=cursor.fetchall()
    con.close()

    if rows:
        return rows
    else:
        return None

def delete_task(task_id:int,member_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="DELETE FROM todo WHERE task_id=? AND member_id=?"

    cursor.execute(query,(task_id,member_id))

    affected=cursor.rowcount
    con.commit()
    con.close()

    return affected>0