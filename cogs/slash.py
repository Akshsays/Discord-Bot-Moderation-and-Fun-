import discord
import logging
import datetime
from discord.ext import commands
from discord import app_commands

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot_logger')

class Moderation(commands.Cog): # Creating a class and inherit commands.Cog 
    
    def __init__(self,bot):
        self.bot=bot # Constructor that stores/load bot for later use

    @app_commands.command(name="ban",description="Ban user form server")
    @app_commands.describe(user="The user to ban", reason="The reason for ban")
    async def ban_slash(self,interaction:discord.Interaction,user:discord.Member,reason:str):

        if interaction.guild.me.guild_permissions.ban_members is False:
            await interaction.response.send_message(f"I don't have ban permissions",ephemeral=True)
            return
        
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(f"{interaction.user.mention} You don't have permission to ban",ephemeral=True)
            return

        if interaction.user==user:
            await interaction.response.send_message("You can't ban yourself!!",ephemeral=True)
            return
            
        try:
            try:
                await user.send(f"You have been banned from {interaction.guild.name} due to: {reason}")

            except discord.Forbidden:
                pass # User has DMs disabled so pass and ban

            await user.ban(reason=reason)
            await interaction.response.send_message(f"{user} has been banned for: {reason}", ephemeral=True)

        except discord.NotFound:
            await interaction.response.send_message("User not found", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Failed to ban", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Something went wrong", ephemeral=True)

    @app_commands.command(name="unban",description="Unban user")
    @app_commands.describe(user_id="user id of banned user",reason="reason to unban")
    async def unban_slash(self,interaction:discord.Interaction,user_id: str,reason:str="Not provided"):

        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(f"You don't have sufficent perms to unban!!",ephemeral=True)
            return

        if interaction.guild.me.guild_permissions.ban_members is False:
            await interaction.response.send_message(f"I don't have permission to unban!!",ephemeral=True)
            return

        if str(interaction.user.id)==user_id:
            await interaction.response.send_message(f"You are not banned idiot!!",ephemeral=True)
            return
        
        try:
            await interaction.guild.unban(discord.Object(id=user_id),reason=reason)
            await interaction.response.send_message(f"Unbanned user {user_id} by {interaction.user} reason:{reason}",ephemeral=True)

        except discord.NotFound:
            await interaction.response.send_message(f"Member not found or banned!!",ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"I don't have the permission to unban the user or they aren't unbanned!!",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong!!",ephemeral=True)

    
    @app_commands.command(name="kick",description="kick user from server")
    @app_commands.describe(user="User to kick",reason="Reason to kick")
    async def kick(self,interaction:discord.Interaction,user:discord.Member,*,reason: str="Not provided"):

        if interaction.guild.me.guild_permissions.kick_members is False:
            await interaction.response.send_message(f"I don't have permissions to kick",ephemeral=True)
            return

        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message(f"You don't have permissions to kick",ephemeral=True)
            return

        if interaction.user==user:
            await interaction.response.send_message(f"You can't kick yourself",ephemeral=True)
            return

        try:
            try:
                await user.send(f"You have been kicked from {interaction.guild.name}. Reason: {reason}")
            except discord.Forbidden:
                pass # User has DMs disabled so pass and ban

            await user.kick(reason=reason) # user.kick only accept reason
            await interaction.response.send_message(f"{user.mention} is kicked from server",ephemeral=True)

        except discord.NotFound:
            await interaction.response.send_message(f"Mentioned user not found",ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"Failed to kick",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong",ephemeral=True)

    @app_commands.command(name="report", description="Report the user")
    @app_commands.describe(message_link="The message to be reported", user="User to report", reason="Reason to report")
    async def report(self, interaction: discord.Interaction, user: discord.Member,*, message_link: str, reason: str,):

        if interaction.user==user:
                await interaction.response.send_message("Want to report yourself dumbo?",ephemeral=True)
                return

        if user.bot:
            await interaction.response.send_message("Can't report a application",ephemeral=True)
            return
        
        report_embed=discord.Embed(
            title="Report Message",
            description=f"{interaction.user.mention} reported {user.mention} for reason:{reason}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        report_embed.add_field(name="Message / Evidence",value=message_link)
        report_embed.set_footer(text=f"Report ID: {interaction.id}")

        target_channel=1509269032572813505
        log_channel=interaction.guild.get_channel(target_channel) # get channel from guild cache

        if log_channel is False:
                await interaction.response.send_message("Target channel not found/cached",ephemeral=True) 
                return

        try:
            try:
                await interaction.user.send(embed=report_embed)
            except discord.Forbidden:
                pass

            await log_channel.send(embed=report_embed)
            await interaction.response.send_message("Thanks for reporting",ephemeral=True)

        except Exception as e:
            print(f"Report error: {e}")
            await interaction.response.send_message("Something went wrong",ephemeral=True)


    @app_commands.command(name="timeout",description="Mute user for specific duration")
    @app_commands.describe(user="User to mute",duration="Duration of timeout (minutes)",reason="Reason to mute")
    async def mute(self,interaction: discord.Interaction, user: discord.Member, duration:int,*, reason: str="Not provided"):

        if not interaction.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message("I don't have permissions to mute",ephemeral=True)
            return

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You don't have permissions to mute",ephemeral=True)
            return

        if interaction.user==user:
            await interaction.response.send_message("You can't mute yourself",ephemeral=True)
            return
        
        if user.bot:
            await interaction.response.send_message("No use of muting bot",ephemeral=True)
            return

        try:
            # Get the time when command was run and caculate until time after that, Timedelta interprets number into exact minutes.
            timeout_until=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=duration) 

            await user.timeout(timeout_until,reason=reason)
            await interaction.response.send_message(f"{user.mention} muted succesfully",ephemeral=True)

        except discord.NotFound:
            await interaction.response.send_message("Mentioned user not found",ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("failed to mute, user has too much aura",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Something went wrong",ephemeral=True)

    
    @app_commands.command(name="removetimeout",description="Unmute User in server")
    @app_commands.describe(user="User to unmute")
    async def removetimeout(self,interaction: discord.Interaction, user: discord.Member):

        if not interaction.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message("I don't have permissions to mute",ephemeral=True)
            return

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You don't have permissions to use this command",ephemeral=True)
            return
        
        if interaction.user==user:
            await interaction.response.send_message("You are not muted!",ephemeral=True)
            return

        if user.bot:
            await interaction.response.send_message("Never muted a bot at first place",ephemeral=True)
            return

        # Check if user was ever muted or not
        if user.timed_out_until is None or user.timed_out_until <= discord.utils.utcnow():
            await interaction.response.send_message(f"{user.mention} was never muted",ephemeral=True)
            return

        try:

            await user.edit(timed_out_until=None)
            await interaction.response.send_message(f"Succesfully Unmuted {user.mention}",ephemeral=True)

        except discord.NotFound:
            await interaction.response.send_message("Target not found or left the server",ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permissions to modify this user timeout",ephemeral=True)
        except Exception as e:
            print(f"error:{e}")
            await interaction.response.send_message("Something went wrong while excecuting command",ephemeral=True)

    @app_commands.command(name="embed",description="Create Embeds")
    @app_commands.describe(title="Title for embed",description="Description for embed",footer="Add footer",channel="Channel for embed to be posted")
    async def embed(self, interaction:discord.Interaction,title: str, description:str,footer:str,channel:discord.TextChannel):

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(f"{interaction.user.mention} you lack `manage_message` permissions",ephemeral=True)
            return
        
        if not interaction.guild.me.guild_permissions.embed_links:
            await interaction.response.send_message(f"{interaction.user.mention} you lack `manage_message` permissions",ephemeral=True)
            return

        permissions=channel.permissions_for(interaction.guild.me) # Get all permissions a bot has in a channel

        if not permissions.send_messages:
            await interaction.response.send_message("I don't have permissions to write/view channel",ephemeral=True) 
            return

        embed=discord.Embed(
            title=title,
            description=description,
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )

        embed.set_footer(text=footer)
        
        try:
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Succesfully sent embed in {channel.mention}",ephemeral=True)
        
        except Exception as e:
            print(f"error {e}")
            await interaction.response.send_message("Something went wrong",ephemeral=True)
            
    

async def setup(bot):
    await bot.add_cog(Moderation(bot))


