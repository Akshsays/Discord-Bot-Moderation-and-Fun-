import discord 
import datetime
from discord.ext import commands
from discord import app_commands

class Prefix(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(name="ping")
    async def pingu(self,ctx):
        await ctx.send('pong')

    @commands.command(name="ban")
    async def ban(self,ctx,member:discord.Member,*,reason: str ="Not provided"):

        # member==user
        if ctx.author==member:
            await ctx.send('You cant ban yourself',delete_after=10)
            return

        # Bot has permissions or not
        if ctx.guild.me.guild_permissions.ban_members is False:
            await ctx.send(f"{ctx.author.name}, I don't have permission to ban!!",delete_after=10)
            return

        # If user has permission to execute 
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send(f"{ctx.author.name}, you don't have permission to ban!!",delete_after=10)
            return

        try:

            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.name} for reason: {reason}",delete_after=10)

        except discord.NotFound:
            await ctx.send("User not found",delete_after=10)
        except discord.Forbidden:
            await ctx.send("Looks like user has higher or equal role as mine",delete_after=10)
        except Exception as e:
            await ctx.send("Something went wrong",delete_after=10)


    @commands.command(name="unban")
    async def unban(self,ctx,user_id: str,*,reason: str="Not provided"):
        
        if ctx.guild.me.guild_permissions.ban_members is False:
            await ctx.send(f"Sorry i don't have permissions to ban!!",delete_after=10)
            return

        if str(ctx.author.id)==user_id:
            await ctx.send("You were never banned!!",delete_after=10)
            return

        if not ctx.author.guild_permissions.ban_members:
          await ctx.send(f"{ctx.author.name}, you don't have ban permissions!!",delete_after=10)
          return

        try:
            user_id_int=int(user_id)
            user = await ctx.bot.fetch_user(user_id) # we need to use bot.fetch_user
            await ctx.guild.unban(user,reason=reason) # telling discord which server & who to unban

            await ctx.send(f"Unbanned {user.name} for {reason}",delete_after=10)


        except ValueError:
            await ctx.send("Please enter valid user id!!",delete_after=10)
        except discord.NotFound:
            await ctx.send("User not found!!",delete_after=10)
        except discord.Forbidden:
            await ctx.send("Looks like user has higher or equal role as mine",delete_after=10)
        except Exception as e:
            await ctx.send("Something went wrong",delete_after=10)

    @commands.command(name="kick")
    async def kick(self,ctx,user:discord.Member,*,reason="Not provided"):

            if ctx.guild.me.guild_permissions.kick_members is False:
                await ctx.send("I don't have kick perms",delete_after=10)
                return

            if not ctx.author.guild_permissions.kick_members:
                await ctx.send("You don't have kick perms",delete_after=10)
                return

            if ctx.author==user:
                await ctx.send("You can't kick yourself",delete_after=10)
                return

            try:
                try:
                    await user.send(f"You have been kicked from {ctx.guild.name}. Reason: {reason}")
                except discord.Forbidden:
                    pass # User has DMs disabled so pass and ban

                await user.kick(reason=reason)
                await ctx.send(f"Successfully kicked {user.mention} for the reason: {reason}",delete_after=10)

            except discord.NotFound:
                await ctx.send("User not found to ban",delete_after=10)
            except discord.Forbidden:
                await ctx.send("I don't have kick perms or user has higher role than mine",delete_after=10)
            except Exception as e:
                await ctx.send("Something went wrong!!",delete_after=10)

    @commands.command(name="mute")
    async def timeout(self,ctx,user: discord.Member,duration :int,*,reason: str="Not provided"):

        if not ctx.guild.me.guild_permissions.moderate_members:
            await ctx.send("I don't have moderate member permission",delete_after=10)
            return

        if not ctx.author.guild_permissions.moderate_members:
            await ctx.send("You don't have timeout perms",delete_after=10)
            return

        if ctx.author==user:
            await ctx.send("You can't timeout yourself",delete_after=10)
            return

        if user.bot:
            await ctx.send("No use of muting bot",delete_after=10)
            return

        try:
            timeout_unit=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=duration)

            await user.timeout(timeout_unit,reason=reason)
            await ctx.send(f"Succesfully muted {user.mention}!",delete_after=10)
        
        except discord.NotFound:
            await ctx.send("Mentioned user not found",delete_after=10)
        except discord.Forbidden:
            await ctx.send("failed to mute, user has too much aura",delete_after=10)
        except Exception as e:
            await ctx.send("Something went wrong",delete_after=10)

    @commands.command(name="unmute")
    async def unmute(self,ctx,user: discord.Member):

        if not ctx.guild.me.guild_permissions.moderate_members:
            await ctx.send("I don't have moderate member permission",delete_after=10)
            return

        if not ctx.author.guild_permissions.moderate_members:
            await ctx.send("You don't have timeout perms",delete_after=10)
            return

        if ctx.author==user:
            await ctx.send("You can't timeout yourself",delete_after=10)
            return

        if user.bot:
            await ctx.send("No use of muting bot",delete_after=10)
            return

        if user.timed_out_until is None:
            await ctx.send(f"{user.mention} is never muted",delete_after=10)
            return

            # Check if user mute expired naturally 
        if user.timed_out_until <= datetime.datetime.now(datetime.timezone.utc):
            await ctx.send(f"{user.mention} mute expired naturally",delete_after=10)
            return

        try:

            await user.edit(timed_out_until=None)
            await ctx.send(f"Succesfully Unmuted {user.mention}",delete_after=10)

        except discord.NotFound:
            await ctx.send("Target not found or left the server",delete_after=10)
        except discord.Forbidden:
            await ctx.send("I don't have permissions to modify this user timeout",delete_after=10)
        except Exception as e:
            await ctx.send("Something went wrong while excecuting command",delete_after=10)

async def setup(bot):
    await bot.add_cog(Prefix(bot))