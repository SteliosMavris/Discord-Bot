from discord.ext import commands
import random

from cogs.enemies import enemyPotentialSpawn

class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        channel = message.channel
        await enemyPotentialSpawn(channel)
        print(f'Message from {message.author}: {message.content}')

    
# Add cog to the bot
async def setup(bot):
    await bot.add_cog(Events(bot))