import sqlite3

DB_NAME="Suggestionconfig.db"

def get_connected():
    return sqlite3.connect(DB_NAME)

def init_table():

    con=get_connected()
    cursor=con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS suggestion_channels(guild_id INT PRIMARY KEY,channel_id INT NOT NULL,suggester_id INT,suggestion_id INT)")
    
    con.commit()
    cursor.close()

def set_suggestion_channel(guild_id:int,channel_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="INSERT OR REPLACE INTO suggestion_channels(guild_id, channel_id) VALUES(?,?)"
    cursor.execute(query,(guild_id,channel_id))

    con.commit()
    cursor.close()

def store_info(guild_id:int,suggester_id:int,suggestion_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="UPDATE suggestion_channels SET suggester_id=?, suggestion_id=? where guild_id=?"
    cursor.execute(query,(suggester_id,suggestion_id,guild_id))

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

def get_info(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT suggester_id from suggestion_channels WHERE guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone()
    value=int(result[0])
    cursor.close()

    if value:
        suggester_id=value

        return int(suggester_id)
    else:
        return None