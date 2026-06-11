import discord
import datetime
import random
from enum import Enum
from discord.ext import commands
from discord import app_commands

class ButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=180) # Optional timeout

        

        @discord.ui.button(label="Rock", style=discord.ButtonStyle.primary,emoji="🪨")
        async def rock_Button(self, interaction: discord.Interaction, button: discord.ui.Button):

            c=["Rock","Paper","Scissor"]
            comp_choice=random.choice(c)

            if comp_choice=="Rock":
                await interaction.response.send_message("Well we tied", ephemeral=True)
            elif comp_choice=="Paper":
                await interaction.response.send_message("Computer win", ephemeral=True)
            elif comp_choice=="Scissor":
                await interaction.response.send_message("ggs you won", ephemeral=True)

        
        @discord.ui.button(label="Paper", style=discord.ButtonStyle.primary,emoji="🗞️")
        async def paper_Button(self, interaction: discord.Interaction, button: discord.ui.Button):

            c=["Rock","Paper","Scissor"]
            comp_choice=random.choice(c)

            if comp_choice=="Paper":
                await interaction.response.send_message("Well we tied", ephemeral=True)
            elif comp_choice=="Rock":
                await interaction.response.send_message("ggs you win", ephemeral=True)
            elif comp_choice=="Scissor":
                await interaction.response.send_message("computer won", ephemeral=True)
        
        @discord.ui.button(label="Scissor", style=discord.ButtonStyle.primary,emoji="✂️")
        async def Rock_Button(self, interaction: discord.Interaction, button: discord.ui.Button):

            c=["Rock","Paper","Scissor"]
            comp_choice=random.choice(c)

            if comp_choice=="Rock":
                await interaction.response.send_message("computer won", ephemeral=True)
            elif comp_choice=="Paper":
                await interaction.response.send_message("ggs you win", ephemeral=True)
            elif comp_choice=="Scissor":
                await interaction.response.send_message("Well we tied", ephemeral=True)

    @app_commands.command(name="rps-game", description="play rps games")
    async def buttoncall(self,interaction:discord.Interaction):
        rps_embed=discord.Embed(
            title="**RPS Game**",
            description="You vs Computer",
            timestamp=discord.utils.utcnow()
        )
        icon=interaction.user.display_avatar.url
        rps_embed.set_footer(text=interaction.user,icon_url=icon)
        await interaction.response.send_message(embed=rps_embed, view=self.MyView())

    @commands.command()
    async def rps(self, ctx):
        rps_embed=discord.Embed(
            title="**RPS Game**",
            description="You vs Computer",
            timestamp=discord.utils.utcnow()
        )
        icon=ctx.author.display_avatar.url
        rps_embed.set_footer(text=ctx.author,icon_url=icon)
        await ctx.send(embed=rps_embed, view=self.MyView())

async def setup(bot):
    await bot.add_cog(ButtonCog(bot))   