import discord 
import datetime
import utls.reportconfig 
import traceback
from utls.reportconfig import init_table,init_member,set_report_channel,get_report_channel,get_user,set_member
from discord.ext import commands
from discord import app_commands


class Report(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        init_table() # call table function to create a empty table it 
        init_member()

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=180) # Optional timeout

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary,emoji="✅")
        async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):

            try:
                target=get_user(interaction.guild.id)
                user=interaction.guild.get_member(target)
                if user is None:
                    user=await interaction.guild.fetch_member(target)
                if user:
                    await user.send(f"hey {user.mention} your report has been accepted")
                    await interaction.response.send_message("Report processed",ephemeral=True)
            except discord.Forbidden:
                pass
            except Exception as e:
                print(e)


        @discord.ui.button(label="Decline", style=discord.ButtonStyle.primary,emoji="❌")
        async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                target=get_user(interaction.guild.id)   
                user=interaction.guild.get_member(target)
                if user is None:
                    user=await interaction.guild.fetch_member(target)
                else:
                    pass
                if user:
                    await user.send(f"hey {user.mention} your report has been declined")
                    await interaction.response.send_message("Report processed",ephemeral=True)  
            except discord.Forbidden:
                pass
            except Exception as e:
                print(e)
        

    @app_commands.command(name="report-config",description="Configure report channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(channel="Set report channel")
    async def reportconfig(self,interaction:discord.Interaction,channel:discord.TextChannel):

            set_report_channel(interaction.guild.id,channel.id) # call set_report_channel function to set desired channel

            await interaction.response.send_message(f"Report channel set to {channel.mention}",ephemeral=True)

    
    @app_commands.command(name="view-report-channel",description="Get the configured channel for reports")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.default_permissions(administrator=True)
    async def viewconfig(self,interaction:discord.Interaction):

        report_channel=get_report_channel(interaction.guild.id) # access the report channel by calling get_report_channel

        log_channel=interaction.guild.get_channel(report_channel) # get the channel object for specific id

        await interaction.response.send_message(f"Current report config channel is- {log_channel.mention}",ephemeral=True)


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
            reporter=set_member(interaction.guild.id,interaction.user.id)
            if interaction.guild: # if guild exist 
                target_channel_id=get_report_channel(interaction.guild.id) # call the get report function to access the report_channel id
            else:
                await interaction.response.send_message("Command can only be run in guild")
                return

            if not target_channel_id: # if target channel id row not found
                await interaction.response.send_message(f"Channel not configured",ephemeral=True)
                return
                
            log_channel=interaction.guild.get_channel(target_channel_id) # get the channel object for report channel

            if not log_channel: # if channel not found 
                try:

                    target_channel= await interaction.guild.fetch_channel(target_channel_id) # fetch from guild cache 
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

        report_embed=discord.Embed(
            title="Report Message",
            description=f"{interaction.user.mention} reported {user.mention} for reason:{reason}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        
        report_embed.add_field(name="Message / Evidence",value=message_link)
        report_embed.set_footer(text=f"Report ID: {interaction.id}")

        try:
            await interaction.user.send(f"Thanks for reporting {user.mention}",embed=report_embed)
        except discord.Forbidden:
            pass
        except Exception as e:
            print(e)

        try:
            await log_channel.send(embed=report_embed,view=self.MyView())
            await interaction.response.send_message(f"Succesfully reported {user.mention}",ephemeral=True)

        except Exception as e:
            print(e)
            error = e
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            formatted_tb = "\n" + "".join(tb) + "\n"
            print(formatted_tb)
            if not interaction.response.is_done():
                await interaction.response.send_message("Something went wrong",ephemeral=True)


async def setup(bot):
    await bot.add_cog(Report(bot))