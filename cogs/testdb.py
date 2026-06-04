import discord
import sqlite3
from discord.ext import commands
from discord import app_commands

database= sqlite3.connect('testing.db') ## connect with database
cursor= database.cursor() # row by row proccesing of result
database.execute("CREATE TABLE IF NOT EXISTS message(messages_content STRING, message_id INT)") # execute some command

class testdb(commands.Cog):
    
    def __init__(self,bot):
        self.bot=bot

    @app_commands.command(name="write",description="writing command")
    @app_commands.describe(message="enter message")
    async def write(self,interaction:discord.Interaction, message:str):

        query="INSERT INTO message VALUES (?,?)" # query 
        cursor.execute(query,(message,interaction.id)) # row by row proccesing of the message and id
        database.commit() # commit changes 

        await interaction.response.send_message("Message sent to database",ephemeral=True)

    @app_commands.command(name="show",description="show command")
    async def write(self,interaction:discord.Interaction):

        query="SELECT * FROM message" # query 
        data=cursor.execute(query).fetchall() # row by row proccesing of the message and id
        database.commit() # commit changes 

        await interaction.response.send_message(data,ephemeral=True)

async def setup(bot):
    await bot.add_cog(testdb(bot))