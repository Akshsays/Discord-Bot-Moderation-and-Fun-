import discord
import datetime
import traceback
import utls.suggestionconfig
from utls.suggestionconfig import init_table,store_info,review_info,get_info,store_suggestion_messageid,get_message_id,set_suggestion_channel,get_suggestion_channel,get_suggestion_message
from discord.ext import commands
from discord import app_commands
from discord import ui


class Suggestions(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        init_table()

    class MyView(discord.ui.View):

        def __init__(self):
            super().__init__(timeout=180)

        class MyModal(discord.ui.Modal):
            reason=discord.ui.TextInput(
            label="Reason",
            placeholder="Enter reason...",
            max_length=1000
            )
            def __init__(self,title):
                self.title=title
                super().__init__(title=title)

            async def on_submit(self, interaction: discord.Interaction):

                if self.title=="Suggestion Accepted":
                    color=discord.Color.green()
                elif self.title=="Suggestion Considered":
                    color=discord.Color.yellow()
                else:
                    color=discord.Color.red()

                embed = discord.Embed(title="Suggestion review",description=f"**{self.title} by {interaction.user.global_name}**",color=color)
                embed.add_field(name="Status", value=self.title)
                embed.add_field(name="Reason", value=self.reason.value)

                review_status=self.title
                review_reason=self.reason.value
                suggester_id=get_info(interaction.guild.id)
                message=get_suggestion_message(interaction.guild.id)
                message_id=get_message_id(interaction.guild.id)
                channel_id=get_suggestion_channel(interaction.guild.id)

                reviwer=review_info(interaction.guild.id,interaction.user.id,review_status,review_reason)

                new_suggestion_embed=discord.Embed(
                    title="Suggestion",
                    description=f"{message} \n **{review_status} by {interaction.user.global_name}**",
                    color=color
                )
                
                new_suggestion_embed.add_field(name="Status:",value=review_status)
                new_suggestion_embed.add_field(name="Reason:",value=review_reason)
                try:
                    
                    log_channel=interaction.guild.get_channel(channel_id)

                    if not log_channel:
                        try:
                            target= await interaction.guild.fetch_channel(channel_id)
                        except Exception as e:
                            pass
                    try:
                        sug_message= await log_channel.fetch_message(message_id)
                    except Exception as e:
                        print(e)

                    await sug_message.edit(embed=new_suggestion_embed)

                except Exception as e:
                    print(e)


                try:
                    target=get_info(interaction.guild.id)
                    dm_user=interaction.guild.get_member(target)
                    if dm_user is None:
                        user=await interaction.guild.fetch_member(target)
                    if user:
                        await user.send(embed=embed)
                        await interaction.response.send_message("Suggestion updated",ephemeral=True)
                        
                except discord.Forbidden:
                    pass
                except Exception as e:
                    print(e)

        @discord.ui.button(label="Accept",style=discord.ButtonStyle.success)
        async def accept(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.send_modal(self.MyModal("Suggestion Accepted"))

        @discord.ui.button(label="Consider",style=discord.ButtonStyle.secondary)
        async def consider(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.send_modal(self.MyModal("Suggestion Considered"))

        @discord.ui.button(label="Decline",style=discord.ButtonStyle.red)
        async def decline(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.send_modal(self.MyModal("Suggestion Declined"))


    @app_commands.command(name="suggestion-config",description="Configure suggestion channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(channel="Set suggestion channel")
    async def suggestionconfig(self,interaction:discord.Interaction,channel:discord.TextChannel):

        set_suggestion_channel(interaction.guild.id,channel.id)

        await interaction.response.send_message(f"Report channel set to {channel.mention}",ephemeral=True)

    @app_commands.command(name="view-suggestion-config",description="Get the configured channel for suggestion")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.default_permissions(administrator=True)
    async def viewconfig(self,interaction:discord.Interaction):

        suggestion_channel=get_suggestion_channel(interaction.guild.id) # access the report channel by calling get_report_channel

        log_channel=interaction.guild.get_channel(suggestion_channel) # get the channel object for specific id

        await interaction.response.send_message(f"Current suggestion config channel is- {log_channel.mention}",ephemeral=True)
        
    @app_commands.command(name="suggest",description="Suggest to moderators")
    @app_commands.describe(suggestion="Enter suggestion to submit")
    async def suggest(self,interaction:discord.Interaction,*,suggestion:str):


        try:
            info=store_info(interaction.guild.id,suggestion,interaction.user.id)
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
            sent_message=await log_channel.send(embed=suggestionembed,view=self.MyView())
            await interaction.response.send_message(f"Suggestion succesfully submitted",ephemeral=True)
            message_id=store_suggestion_messageid(interaction.guild.id,sent_message.id)
            # await sent_message.create_thread(name="Suggestion Thread")
        
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