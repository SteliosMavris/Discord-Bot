import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
import random
from utils.database import add_souls, add_user, get_user_stats, isUserInDatabase, upgrade

GUILD_ID = 1254407988953878579

class Commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name="praise", description="Earn souls by praising the sun.")    # Name the slash command and give a description
    @app_commands.guilds(discord.Object(id=GUILD_ID))                                      # Attach to the specific guild
    @app_commands.checks.cooldown(rate=1, per=3600, key=lambda i: (i.guild_id, i.user.id)) # Member cooldown of 1 hour
    async def praiseTheSun(self, interaction: discord.Interaction):
        # Calculate reward
        chance = random.randint(1, 100)
        if chance >= 1 and chance < 85:
            start = 1000
            end = 2500
            message = "The sun's radiance rewards {user} with"
        elif chance >= 85 and chance < 95:
            start = 2600
            end = 5000
            message = "The sun smiles upon your worship. It rewards {user} with"
        elif chance >= 95 and chance < 100:
            start = 5100
            end = 7000
            message = "The sun's brilliance grants you great warmth! It rewards {user} generously with"
        else:
            start = 7100
            end = 9000
            message = "The sun is thrilled from your unending devotion! It blesses {user} with"
        
        reward = random.randint(start, end)

        # Defer the response to give more time
        await interaction.response.defer()

        # Send the first message with "Praising the sun" and the GIF
        with open("data/praise_the_sun.gif", "rb") as gif_file:
            await interaction.followup.send(
                content="Praising the sun \\O/",
                file=discord.File(gif_file, filename="praise_the_sun.gif")
            )

        # Personalize the message with the user's name
        personalized_message = message.format(user=interaction.user.name)
        await interaction.followup.send(f"{personalized_message} **{reward} souls**")
        add_souls(interaction.user.id,reward)

    @praiseTheSun.error
    async def cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"This command is on cooldown. Try again in {(error.retry_after/60):.0f} minutes.", ephemeral=True)
        else:
            raise error

    @app_commands.command(name="upgrade", description="Upgrade your character's stats")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(stat="Stat to upgrade in lowercase")
    @app_commands.choices(
        stat=[
            app_commands.Choice(name="vitality", value="vitality"),
            app_commands.Choice(name="attunement", value="attunement"),
            app_commands.Choice(name="endurance", value="endurance"),
            app_commands.Choice(name="strength", value="strength"),
            app_commands.Choice(name="dexterity", value="dexterity"),
            app_commands.Choice(name="resistance", value="resistance"),
            app_commands.Choice(name="intelligence", value="intelligence"),
            app_commands.Choice(name="faith", value="faith"),
        ]
    )
    async def upgrade_stats(self, interaction: discord.Interaction, stat: app_commands.Choice[str]):
        upgrade(interaction.user.id, stat.value, interaction)
        print("Used upgrade!")
        await interaction.response.send_message(f"Leveled up {stat.value}!")


    @app_commands.command(name="stats", description="See your stats")
    @app_commands.guilds(discord.Object(id=GUILD_ID))  # Attach to the specific guild
    async def stats(self, interaction: discord.Interaction):
    # Generate embed and print it
        if not isUserInDatabase(interaction.user.id):
            add_user(interaction.user.id)
        user_stats = get_user_stats(interaction.user.id)
        
        userID, level, souls, vitality, attunement, endurance, strength, dexterity, resistance, intelligence, faith, humanity = user_stats
        print("Initialised user stats!")
        embed = discord.Embed(title=f"{interaction.user.name}'s Status", description="Check status", color=discord.Color.green())
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/dark-souls/images/4/4d/Lordran.jpg/revision/latest?cb=20160716014132&path-prefix=es")
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="Souls", value=souls, inline=True)
        embed.add_field(name="Vitality", value=vitality, inline=False)
        embed.add_field(name="Attunement", value=attunement, inline=False)
        embed.add_field(name="Endurance", value=endurance, inline=False)
        embed.add_field(name="Strength", value=strength, inline=False)
        embed.add_field(name="Dexterity", value=dexterity, inline=False)
        embed.add_field(name="Resistance", value=resistance, inline=False)
        embed.add_field(name="Intelligence", value=intelligence, inline=False)
        embed.add_field(name="Faith", value=faith, inline=False)
        embed.add_field(name="Humanity", value=humanity, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="equipment", description="View your weapons and armour")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def inventory(self, interaction: discord.Interaction):
        if not isUserInDatabase(interaction.user.id):
            add_user(interaction.user.id)
        embed = discord.Embed(title=f"{interaction.user.name}'s equipment", description="Check equipment", color=discord.Color.green())
        embed.add_field(name="Helm", value="None", inline=False)
        embed.add_field(name="Physical Def", value=0, inline=False)
        embed.add_field(name="Magic Def", value=0, inline=False)
        embed.add_field(name="Fire Def", value=0, inline=False)

        embed.add_field(name="", value="", inline=False) 

        embed.add_field(name="Chest", value="None", inline=False)
        embed.add_field(name="Physical Def", value=0, inline=False)
        embed.add_field(name="Magic Def", value=0, inline=False)
        embed.add_field(name="Fire Def", value=0, inline=False)
        embed.add_field(name="", value="", inline=False)
                
        embed.add_field(name="Gauntlets", value="None", inline=False)
        embed.add_field(name="Physical Def", value=0, inline=False)
        embed.add_field(name="Magic Def", value=0, inline=False)
        embed.add_field(name="Fire Def", value=0, inline=False)

        embed.add_field(name="", value="", inline=False)

        embed.add_field(name="Leggings", value="None", inline=False)
        embed.add_field(name="Physical Def", value=0, inline=False)
        embed.add_field(name="Magic Def", value=0, inline=False)
        embed.add_field(name="Fire Def", value=0, inline=False)

        await interaction.response.send_message(embed=embed)

# Add cog to the bot
async def setup(bot):
    await bot.add_cog(Commands(bot))