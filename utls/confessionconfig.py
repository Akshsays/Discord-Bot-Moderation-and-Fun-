import sqlite3

DB_NAME="Confessionconfig.db"

def get_connected():
    return sqlite3.connect(DB_NAME)

def init_table():

    con=get_connected()
    cursor=con.cursor()

    con.execute("CREATE TABLE IF NOT EXISTS confession_config(guild_id INT PRIMARY KEY,confession_channel INT NOT NULL,member_id INT,confession STRING)")

    con.commit()
    con.close()

def setup_channel(guild_id:int,confession_channel:int):

    con=get_connected()
    cursor=con.cursor()

    query="INSERT OR REPLACE INTO confession_config(guild_id,confession_channel) VALUES(?,?)"
    con.execute(query,(guild_id,confession_channel))

    con.commit()
    con.close()

def get_confession_channel(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT confession_channel FROM confession_config WHERE guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone()
    value=int(result[0])
    cursor.close()

    if value:
        channel_id=value

        return int(channel_id)
    else:
        return None
