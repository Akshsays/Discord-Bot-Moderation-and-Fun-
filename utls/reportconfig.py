import sqlite3


DB_NAME="Reportconfig.db"

def get_connected():
    return sqlite3.connect(DB_NAME)

def init_table():

    con=get_connected()
    cursor=con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS report_channels(guild_id INT PRIMARY KEY,report_channel INT NOT NULL)")
    
    con.commit()
    cursor.close()

def init_member():
    con=get_connected()
    cursor=con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS member_info(guild_id INT PRIMARY KEY,reporter_id INT NOT NULL)")
    
    con.commit()
    cursor.close()

def set_member(guild_id:int,reporter_id):
    con=get_connected()
    cursor=con.cursor()

    query="INSERT OR REPLACE INTO member_info VALUES(?,?)"
    cursor.execute(query,(guild_id,reporter_id))

    con.commit()
    cursor.close()

def get_user(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT reporter_id from member_info where guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone() # fetch the row
    value = int(result[0]) # convert the result from tuple to int 
    cursor.close()

    if value:
        user_id=value

        return int(user_id) if user_id is not None else None

def set_report_channel(guild_id:int,report_channel:int):

    con=get_connected()
    cursor=con.cursor()

    query="INSERT OR REPLACE INTO report_channels VALUES(?,?)"
    cursor.execute(query,(guild_id,report_channel))

    con.commit()
    cursor.close()

def get_report_channel(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT report_channel from report_channels where guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone() # fetch the row
    value = int(result[0]) # convert the result from tuple to int 
    cursor.close()

    if value:
        channel_id=value

        return int(channel_id) if channel_id is not None else None
    else:
        return None
