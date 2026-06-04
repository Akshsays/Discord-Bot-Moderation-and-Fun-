import discord
import datetime
import traceback
import utls.suggestiondb
from utls.suggestiondb import init_table,set_suggestion_channel,get_suggestion_channel
from discord.ext import commands
from discord import app_commands


class Suggestions(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        init_table()

    @app_commands.command(name="suggestion-config",description="Configure suggestion channel")
    @app_commands.describe(channel="Set suggestion channel")
    async def suggestionconfig(self,interaction:discord.Interaction,channel:discord.TextChannel):

        set_suggestion_channel(interaction.guild.id,channel.id)

        await interaction.response.send_message(f"Report channel set to {channel.mention}",ephemeral=True)

    @app_commands.command(name="view-suggestion-config",description="Get the configured channel for suggestion")
    async def viewconfig(self,interaction:discord.Interaction):

        suggestion_channel=get_suggestion_channel(interaction.guild.id) # access the report channel by calling get_report_channel

        log_channel=interaction.guild.get_channel(suggestion_channel) # get the channel object for specific id

        await interaction.response.send_message(f"Current suggestion config channel is- {log_channel.mention}",ephemeral=True)
        
    @app_commands.command(name="suggest",description="Suggest to moderators")
    @app_commands.describe(suggestion="Enter suggestion to submit")
    async def suggest(self,interaction:discord.Interaction,*,suggestion:str):


        try:

            if interaction.guild:
                target_channel_id=get_suggestion_channel(interaction.guild.id)
            else:
                await interaction.response.send_message(f"Command can only be used in a guild",ephemeral=True)
                return

            if not target_channel_id:
                await interaction.response.send_message("Channel not configured",ephemeral=True)
                return

            log_channel=interaction.guild.get_channel(target_channel_id)

            if not log_channel:
                try:
                    suggestion_channel=interaction.guild.fetch_channel(target_channel_id)
                except discord.NotFound:
                    await interaction.response.send_message("Please re-configure because channel is deleted",ephemeral=True)
                    return
                except discord.Forbidden:
                    await interaction.response.send_message("I don't have permissions to access the channel",ephemeral=True)
                    return

        except Exception as e:
            error = e
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            formatted_tb = "\n" + "".join(tb) + "\n"
            print(formatted_tb)
            await interaction.response.send_message("Channel not found or removed",ephemeral=True)
            return

        suggestion_message=suggestion

        suggestionembed=discord.Embed(
            title=f"Suggestion",
            description=suggestion_message,
            timestamp=discord.utils.utcnow(),
            colour=discord.Colour.green()
            )

        icon=interaction.user.display_avatar.url
        suggestionembed.set_footer(text=f"Report ID: {interaction.id} | Sumbitted at")
        suggestionembed.set_author(name=f"{interaction.user.name} - {interaction.user.id}",icon_url=icon)

        try:
            sent_message=await log_channel.send(embed=suggestionembed)
            await interaction.response.send_message(f"Suggestion succesfully submitted",ephemeral=True)
            await sent_message.create_thread(name="Suggestion Thread")
        
        except Exception as e:
            print(e)
            error = e
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            formatted_tb = "\n" + "".join(tb) + "\n"
            print(formatted_tb)
            if not interaction.response.is_done():
                await interaction.response.send_message("Something went wrong",ephemeral=True)

async def setup(bot):
    await bot.add_cog(Suggestions(bot))