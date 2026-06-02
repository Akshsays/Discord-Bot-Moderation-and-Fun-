import discord
import datetime
from discord.ext import commands
from discord import app_commands


class Suggestions(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        
    @app_commands.command(name="suggest",description="Suggest to moderators")
    @app_commands.describe(message="Enter suggestion to submit")
    async def suggest(self,interaction:discord.Interaction,*,message:str):
        
        suggestion_message=message
        suggestionembed=discord.Embed(
            title=f"Suggestion",
            description=suggestion_message,
            timestamp=discord.utils.utcnow(),
            colour=discord.Colour.green()
        )

        icon=interaction.user.display_avatar.url
        suggestionembed.set_footer(text=f"Report ID: {interaction.id} | Sumbitted at")
        suggestionembed.set_author(name=f"{interaction.user.name} - {interaction.user.id}",icon_url=icon)

        suggestion_channel=1510966998824124527
        log_channel=interaction.guild.get_channel(suggestion_channel)


        sent_message=await log_channel.send(embed=suggestionembed)
        await interaction.response.send_message(f"Suggestion succesfully submitted",ephemeral=True)
        await sent_message.create_thread(name="Suggestion Thread")

    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.author==self.bot.user:
            return
        else:
            suggestion_channel=1510966998824124527

            if message.channel.id==suggestion_channel:
                    store_suggestion=message.content
                    Suggestions_embed=discord.Embed(
                        title="Suggestion",
                        description=store_suggestion,
                        timestamp=discord.utils.utcnow(),
                        colour=discord.Colour.green()
                    )
                    
                    icon=message.author.display_avatar
                    Suggestions_embed.set_footer(text=f"Report ID: {message.id} | Sumbitted at")
                    Suggestions_embed.set_author(name=f"{message.author.name} - {message.author.id}",icon_url=icon)
                    

                    await message.delete()
                    sent_message=await message.channel.send(embed=Suggestions_embed)
                    await sent_message.create_thread(name="Suggestion Thread")

async def setup(bot):
    await bot.add_cog(Suggestions(bot))