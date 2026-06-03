import discord 
import datetime
import database 
import traceback
from database import init_table,set_report_channel,get_report_channel
from discord.ext import commands
from discord import app_commands


class Report(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        init_table()


    @app_commands.command(name="reportconfig",description="Configure report channel")
    @app_commands.describe(channel="Set report channel")
    async def reportconfig(self,interaction:discord.Interaction,channel:discord.TextChannel):

            set_report_channel(interaction.guild.id,channel.id)

            await interaction.response.send_message(f"Report channel set to {channel.mention}",ephemeral=True)


    @app_commands.command(name="report", description="Report the user")
    @app_commands.describe(message_link="The message to be reported", user="User to report", reason="Reason to report")
    async def report(self, interaction: discord.Interaction, user: discord.Member,*, message_link: str, reason: str):

        if interaction.user==user: 
            await interaction.response.send_message("Want to report yourself dumbo?",ephemeral=True)
            return

        if user.bot:
            await interaction.response.send_message("Can't report a application",ephemeral=True)
            return

        

        try:
            if interaction.guild:
                target_channel_id=get_report_channel(int(interaction.guild.id))
            else:
                await interaction.response.send_message("Command can only be run in guild")

            if not target_channel_id:
                await interaction.response.send_message(f"Channel not configured",ephemeral=True)
                
            log_channel=interaction.guild.get_channel(target_channel_id)

            if not log_channel:
                target_channel=interaction.guild.fetch_channel(log_channel)

        except Exception as e:
            error = e
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            formatted_tb = "\n" + "".join(tb) + "\n"
            print(formatted_tb)
            await interaction.response.send_message("Channel not found or removed",ephemeral=True)
            return

        report_embed=discord.Embed(
            title="Report Message",
            description=f"{interaction.user.mention} reported {user.mention} for reason:{reason}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        
        report_embed.add_field(name="Message / Evidence",value=message_link)
        report_embed.set_footer(text=f"Report ID: {interaction.id}")
        report_embed.set_author(name={interaction.user.name},icon_url=None)

        try:
            await target_channel.send(embed=report_embed)
            await interaction.response.send(f"Succesfully reported {user.mention}",ephemeral=True)

        except Exception as e:
            print(e)
            error = e
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            formatted_tb = "\n" + "".join(tb) + "\n"
            print(formatted_tb)
            if not interaction.response.is_done():
                await interaction.response.send_message("Something went wrong")


async def setup(bot):
    await bot.add_cog(Report(bot))