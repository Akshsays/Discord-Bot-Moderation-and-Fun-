import sqlite3

DB_NAME="Suggestionconfig.db"

def get_connected():
    return sqlite3.connect(DB_NAME)

def init_table():

    con=get_connected()
    cursor=con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS suggestion_channels(guild_id INT PRIMARY KEY,channel_id INT NOT NULL)")
    
    con.commit()
    cursor.close()

def set_suggestion_channel(guild_id:int,channel_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="INSERT OR REPLACE INTO suggestion_channels VALUES(?,?)"
    cursor.execute(query,(guild_id,channel_id))

    con.commit()
    cursor.close()


def get_suggestion_channel(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT channel_id FROM suggestion_channels WHERE guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone()
    value=int(result[0])
    cursor.close()

    if value:
        channel_id=value

        return int(channel_id)
    else:
        return None
