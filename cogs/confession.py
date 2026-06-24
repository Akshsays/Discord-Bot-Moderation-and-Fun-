import discord
import datetime
import utls.confessionconfig
from discord.ext import commands
from discord import app_commands
from utls.confessionconfig import init_table,setup_channel,get_confession_channel


class Confession(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        init_table()


    @app_commands.command(name="confession-config",description="Config the confession channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(channel="Confession channel where the confession will be sent")
    async def confession_config(self,interaction:discord.Interaction,channel:discord.TextChannel):
        
        setup_channel(interaction.guild.id,channel.id)

        await interaction.response.send_message(f"Succesfully set confession channel to {channel.mention}",ephemeral=True)

    
    @app_commands.command(name="view-confession-config",description="Con")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.default_permissions(administrator=True)
    async def view_channel(self,interaction:discord.Interaction):

        confession_channel=get_confession_channel(interaction.guild.id)
        channel_obj=interaction.guild.get_channel(confession_channel)

        if channel_obj is None:
            await interaction.response.send_message(f"Channel not configured",ephemeral=True)

        await interaction.response.send_message(f"Current Confession channel is - {channel_obj.mention}",ephemeral=True)


    @app_commands.command(name="confess",description="Make a confession")
    async def confess(self,interaction:discord.Interaction,*,confession:str):

        try:
            if interaction.guild:
                confession_channel=get_confession_channel(interaction.guild.id)
            else:
                await interaction.response.send_message("Command can only be run in server",ephemeral=True)

            if not confession_channel:
                await interaction.response.send_message("Channel not configured",ephemeral=True)
                return
            
            channel_obj=interaction.guild.get_channel(confession_channel)

            if not channel_obj:
                try:
                    target_channel=interaction.guild.fetch_channel(channel_obj)
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

        confession_embed=discord.Embed(
            title="Confession",
            description=confession,
            timestamp=discord.utils.utcnow(),
            color=discord.Colour.random()
            )

        try:
            log_message=await channel_obj.send(embed=confession_embed)
            await interaction.response.send_message("Confession sent",ephemeral=True)
        except Exception as e:
            print(e)
            error = e
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            formatted_tb = "\n" + "".join(tb) + "\n"
            print(formatted_tb)
            if not interaction.response.is_done():
                await interaction.response.send_message("Something went wrong",ephemeral=True)

async def setup(bot):
    await bot.add_cog(Confession(bot))
