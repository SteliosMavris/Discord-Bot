import os
import discord
from discord.ext import commands
from utils.database import init_db


class Client(commands.Bot):
    async def on_ready(self):      
        print(f'Solaire has been summoned!')
        # Load all cogs from the "cogs" directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"Loaded cog: {filename}")
                except Exception as e:
                    print(f"Failed to load cog {filename}: {e}")
        try:
            guild = discord.Object(id=1254407988953878579)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

intents = discord.Intents.default() 
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

# Define the main function to initialize the database and start the bot
async def main():
    # Initialize the database
    init_db()

    # Run the bot
    await client.start('MTMyMTA3MDQxMjk4MDgxNzk4MA.GzUjJ_.ALdmu0uQNTDyFufILl9AgE6WDOvSYhgHxIXHeQ')

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())