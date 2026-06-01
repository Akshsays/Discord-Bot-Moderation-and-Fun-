import discord
from discord.ext import commands
from discord import app_commands


class Threads(commands.Cog):

    def __init__(self,bot):
        self.bot=bot

    @app_commands.command(name="create-thread",description="Create public threads")
    @app_commands.describe(title="Thread name",channel="Channel for thread")
    async def createthread(self,interaction:discord.Interaction, title:str, channel:discord.TextChannel):

        if not interaction.user.guild_permissions.create_public_threads:
            await interaction.response.send_message("You don't have permissions to create thread",ephemeral=True)
            return
        
        if not interaction.user.guild.me.guild_permissions.create_public_threads:
            await interaction.response.send_message("I don't have permissions to create thread",ephemeral=True)
            return

        if not channel:
            await interaction.response.send_message("Mentioned channel doesn't exist or not cached",ephemeral=True)
            return
        
        permissions=channel.permissions_for(interaction.guild.me) # Get all permissions a bot has in a channel

        if not permissions.view_channel or not permissions.send_messages:
            await interaction.response.send_message("I don't have permissions to write/view channel",ephemeral=True) 
            return

        try:

            mythread=await channel.create_thread(name=title,type=discord.ChannelType.public_thread)
            try:
                if permissions.send_messages_in_threads:
                    await mythread.add_user(interaction.user)

            except discord.Forbidden:
                await interaction.response.send_message(f"Can't add {interaction.user} due to lack of permissions",ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message(f"failed to add mentioned user",ephemeral=True)

            await interaction.response.send_message(f"Thread **{title}** created in {channel.mention}",ephemeral=True)

        except Exception as e:
            print(f"error {e}")
            await interaction.response.send_message("Something went wrong",ephemeral=True) 

    @commands.command(name="createthread")
    async def create_thread(self,ctx, title:str, channel:discord.TextChannel):

        if not ctx.author.guild_permissions.create_public_threads:
            await ctx.send("You don't have permissions to create thread",delete_after=10)
            return
        
        if not ctx.guild.me.guild_permissions.create_public_threads:
            await ctx.send("I don't have permissions to create thread",delete_after=10)
            return

        if not channel:
            await ctx.send("Mentioned channel doesn't exist or not cached",delete_after=10)
            return
        
        permissions=channel.permissions_for(ctx.guild.me) # Get all permissions a bot has in a channel

        if not permissions.view_channel or not permissions.send_messages:
            await ctx.send("I don't have permissions to write/view channel",delete_after=10) 
            return

        try:

            mythread=await channel.create_thread(name=title,type=discord.ChannelType.public_thread)

            try:
                if permissions.send_messages_in_threads:
                    await mythread.add_user(ctx.author)

            except discord.Forbidden:
                pass
            except discord.HTTPException:
                pass

            await ctx.send(f"Thread {title} created in {channel.mention}",delete_after=10)


        except Exception as e:
            print(f"error {e}")
            await ctx.send("Something went wrong",delete_after=10) 

    
async def setup(bot):
    await bot.add_cog(Threads(bot))