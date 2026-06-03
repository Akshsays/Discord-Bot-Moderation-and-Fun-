import discord 
import datetime
from discord.ext import commands
from discord import app_commands


class Report(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @app_commands.command(name="report", description="Report the user")
    @app_commands.describe(message_link="The message to be reported", user="User to report", reason="Reason to report",attachment="Attachment of message")
    async def report(self, interaction: discord.Interaction, user: discord.Member,*, message_link: str, reason: str,attachment:discord.Attachment):

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
        report_embed.set_author(name={interaction.user.name},icon_url=None)
        report_embed.set_image(url=attachment)

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


async def setup(bot):
    await bot.add_cog(Report(bot))