import sqlite3

DB_NAME="Suggestionconfig.db"

def get_connected():
    return sqlite3.connect(DB_NAME)

def init_table():

    con=get_connected()
    cursor=con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS suggestion_config(guild_id INT PRIMARY KEY,channel_id INT NOT NULL,suggestion_message STRING,suggester_id INT,suggestion_message_id INT,reviewer_id INT,status STRING,reason STRINGs)")
    
    con.commit()
    cursor.close()

def set_suggestion_channel(guild_id:int,channel_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="INSERT OR REPLACE INTO suggestion_config(guild_id, channel_id) VALUES(?,?)"
    cursor.execute(query,(guild_id,channel_id))

    con.commit()
    cursor.close()

def store_info(guild_id:int,suggestion_message:str,suggester_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="UPDATE suggestion_config SET suggestion_message=?, suggester_id=? where guild_id=?"
    cursor.execute(query,(suggestion_message,suggester_id,guild_id))

    con.commit()
    cursor.close()

def review_info(guild_id:int,reviewer_id:int,status:str,reason:str):

    con=get_connected()
    cursor=con.cursor()

    query="UPDATE suggestion_config SET reviewer_id=?, status=?, reason=? where guild_id=?"
    cursor.execute(query,(reviewer_id,status,reason,guild_id))

    con.commit()
    cursor.close()

def store_suggestion_messageid(guild_id:int,suggestion_message_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="UPDATE suggestion_config SET suggestion_message_id=? where guild_id=?"
    cursor.execute(query,(suggestion_message_id,guild_id))

    con.commit()
    cursor.close()

def get_suggestion_channel(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT channel_id FROM suggestion_config WHERE guild_id=?"
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

    query="SELECT suggester_id from suggestion_config WHERE guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone()
    value=int(result[0])
    cursor.close()

    if value:
        suggester_id=value

        return int(suggester_id)
    else:
        return None

def get_message_id(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT suggestion_message_id from suggestion_config WHERE guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone()
    value=int(result[0])
    cursor.close()

    if value:
        suggester_id=value

        return int(suggester_id)
    else:
        return None

def get_suggestion_message(guild_id:int):

    con=get_connected()
    cursor=con.cursor()

    query="SELECT suggestion_message from suggestion_config WHERE guild_id=?"
    cursor.execute(query,(int(guild_id),))

    result=cursor.fetchone()
    value=str(result[0])
    cursor.close()

    if value:
        suggester_message=value

        return str(suggester_message)
    else:
        return None