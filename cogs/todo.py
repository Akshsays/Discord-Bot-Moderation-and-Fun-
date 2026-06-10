import discord
import utls.todoconfig
from discord import app_commands
from discord.ext import commands
from utls.todoconfig import init_table,add_task,view_task,delete_task

class Todo(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        init_table()


    @app_commands.command(name="add-task",description="Add todo list")
    
    async def addtodo(self,interaction:discord.Interaction,*,task:str):

        user_id=interaction.user.id
        todos=add_task(user_id,task)

        await interaction.response.send_message(f"Tasl `ID:{todos}` added",ephemeral=True)

    @app_commands.command(name="show-task",description="Show user todo")
    async def showtodo(self,interaction:discord.Interaction):

        user_id=interaction.user.id
        todos=view_task(user_id)

        if not todos:
            await interaction.response.send_message(f"You don't have any pending taks",ephemeral=True)
            return

        response = "**Your To-Do List:**\n"
        for task_id, text in todos:
            response += f"- `{task_id}`: {text}\n"
    
        await interaction.response.send_message(response)

    @app_commands.command(name="delete-task",description="Delete a task from task-list")
    @app_commands.describe(task_id="Enter task id to delete specific  task")
    async def deletetask(self,interaction:discord.Interaction,task_id:int):

        user_id=interaction.user.id
        
        try:
            todos=view_task(user_id)

            if not todos:
                await interaction.response.send_message(f"You don't have any pending taks",ephemeral=True)
                return

            if delete_task(task_id,user_id):
                await interaction.response.send_message(f"Task `{task_id}` deleted succesfully",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Something went wrong...",ephemeral=True)

async def setup(bot):
    await bot.add_cog(Todo(bot))