import discord 
import datetime
from discord.ext import commands
from discord import app_commands


class Embed(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    @app_commands.command(name="embed",description="Create Embeds")
    @app_commands.describe(title="Title for embed",description="Description for embed",footer="Add footer",channel="Channel for embed to be posted")
    async def embed(self, interaction:discord.Interaction,title: str, description:str,footer:str,channel:discord.TextChannel):

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(f"{interaction.user.mention} you lack `manage_message` permissions",ephemeral=True)
            return
        
        if not interaction.guild.me.guild_permissions.embed_links:
            await interaction.response.send_message(f"I lack `embed_links` permissions",ephemeral=True)
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
    await bot.add_cog(Embed(bot))
