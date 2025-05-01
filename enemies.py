import random
import discord
from discord.ext import commands

# Images of each enemy
enemy_images={
    "Hollow": "https://static.wikia.nocookie.net/darksouls/images/2/26/Zombie_swordsman.jpg/revision/latest?cb=20130206090311", # w
    "Undead Soldier": "https://static.wikia.nocookie.net/darksouls/images/2/25/Download_%282%29.jpeg/revision/latest/thumbnail/width/360/height/450?cb=20200527164530", # w
    "Undead Assassin": "https://darksouls.wdfiles.com/local--files/enemies/undead-assassin.jpg", # w
    "Undead Attack Dog": "https://darksouls.wdfiles.com/local--files/enemies/undead-attack-dog.jpg", # w
    "Ent": "https://static.wikia.nocookie.net/darksouls/images/3/32/Demonic_foliage.jpg/revision/latest/scale-to-width-down/250?cb=20130205121723", # w
    "Small Rat": "https://darksouls.wdfiles.com/local--files/enemies/small-undead-rat-large.jpg", # w
    "Skeleton": "https://darksouls.wdfiles.com/local--files/enemies/skeleton-scimitar-large.jpg", # w
    "Balder Knight": "https://static.wikia.nocookie.net/darksouls/images/6/6c/Balder_Knight.jpg/revision/latest?cb=20140703144112", # w
    "Crystal Knight": "https://static.wikia.nocookie.net/darksouls/images/e/e2/Crystal_general.jpg/revision/latest?cb=20130224145016", # w
    "Flaming Attack Dog": "https://darksouls.wdfiles.com/local--files/enemies/flaming-attack-dog.jpg", # w
    "Infested Ghoul": "https://darksouls.wdfiles.com/local--files/enemies/infested-ghoul-sword-large.jpg", # w
    "Giant Skeleton": "https://static.wikia.nocookie.net/darksouls/images/e/e3/Giant_skeleton_swordsman.jpg/revision/latest?cb=20130629092331", # w
    "Large Rat": "https://static.wikia.nocookie.net/darksouls/images/4/4f/Large_undead_rat01..jpg/revision/latest?cb=20130226145621", # w
    "Man Serpent": "https://static.wikia.nocookie.net/darksouls/images/7/72/Serpent_soldier.jpg/revision/latest?cb=20120901233649", # w
    "Bonewheel": "https://darksouls.wdfiles.com/local--files/enemies/skeleton-wheel.jpg", # w
    "Skeleton Beast": "https://darksouls.wdfiles.com/local--files/enemies/skeleton-beast-large.jpg", # w
    "Black Knight": "https://static.wikia.nocookie.net/darksouls/images/7/74/Black_Knight_Sword.jpg/revision/latest?cb=20130707082423", # w
    "Silver Knight": "https://darksouls.wdfiles.com/local--files/enemies/silver-knight-sword-large.jpg", # w
    "Great Stone Knight": "https://static.wikia.nocookie.net/darksouls/images/4/44/Stone_knight.jpg/revision/latest?cb=20130131012157", # w
    "Bounding Demon": "https://darksouls.wdfiles.com/local--files/enemies/bounding-demon-of-izalith-large.jpg", # w
    "Large Mushroom": "https://darksouls.wdfiles.com/local--files/enemies/mushroom-parent-large.jpg" # w
}

common_enemies={
    "Hollow":{
        "physical_def": (77, 159),
        "magic_def": (58, 119),
        "fire_def": (54, 111),
        "HP": (54, 111),
        "soul_reward": (20, 300)
    },
    "Undead Soldier":{
        "physical_def": (103, 212),
        "magic_def": (77, 159),
        "fire_def": (72, 148),
        "HP": (85, 144),
        "soul_reward": (50, 150)
    },
    "Undead Assassin":{
        "physical_def": 121,
        "magic_def": 90,
        "fire_def": 79,
        "HP": 138,
        "soul_reward": 100
    },
    "Undead Attack Dog":{
        "physical_def": (100, 132),
        "magic_def": (75, 99),
        "fire_def": (60, 78),
        "HP": (100, 210),
        "soul_reward": (80, 300)
    },
    "Ent":{
        "physical_def": 173,
        "magic_def": 139,
        "fire_def": 68,
        "HP": (193, 283),
        "soul_reward": 100
    },
    "Small Rat":{
        "physical_def": (68, 114),
        "magic_def": (51, 85),
        "fire_def": (41, 68),
        "HP": (80, 112),
        "soul_reward": (20, 60)
    },
    "Skeleton":{
        "physical_def": (147, 164),
        "magic_def": (91, 104),
        "fire_def": (68, 79),
        "HP": (54, 96),
        "soul_reward": (50, 100)
    },
}

rare_enemies={
    "Balder Knight":{
        "physical_def": (137, 275),
        "magic_def": (100, 200),
        "fire_def": (103, 207),
        "HP": (129, 385),
        "soul_reward": (160, 500)
    },
    "Crystal Knight":{
        "physical_def": (70, 170),
        "magic_def": (50, 80),
        "fire_def": (30, 160),
        "HP": 742,
        "soul_reward": 3000
    },
    "Flaming Attack Dog":{
        "physical_def": 183,
        "magic_def": 199,
        "fire_def": 913,
        "HP": 124,
        "soul_reward": 150
    },
    "Infested Ghoul":{
        "physical_def": 156,
        "magic_def": 117,
        "fire_def": 125,
        "HP": 365,
        "soul_reward": 150
    },
    "Giant Skeleton":{
        "physical_def": 301,
        "magic_def": 231,
        "fire_def": 204,
        "HP": (262, 386),
        "soul_reward": (500, 1000)
    },
    "Large Rat":{
        "physical_def": 130,
        "magic_def": 99,
        "fire_def": 78,
        "HP": 692,
        "soul_reward": 1000
    },
    "Man Serpent":{
        "physical_def": (359, 462),
        "magic_def": (191, 246),
        "fire_def": (161, 207),
        "HP": (430, 537),
        "soul_reward": 500
    }
}

fearsome_enemies={
    "Bonewheel":{
        "physical_def": (239, 348),
        "magic_def": (183, 267),
        "fire_def": (163, 237),
        "HP": (134, 196),
        "soul_reward": (400, 800)
    },
    "Skeleton Beast":{
        "physical_def": 339,
        "magic_def": 259,
        "fire_def": 229,
        "HP": 446,
        "soul_reward": 1500
    },
    "Black Knight":{
        "physical_def": (281, 298),
        "magic_def": (198, 266),
        "fire_def": (221, 295),
        "HP": (497, 887),
        "soul_reward": (800, 1800)
    },
    "Silver Knight":{
        "physical_def": 315,
        "magic_def": 251,
        "fire_def": 212,
        "HP": 464,
        "soul_reward": 1000-1300
    },
    "Great Stone Knight":{
        "physical_def": 446,
        "magic_def": 356,
        "fire_def": 356,
        "HP": 190,
        "soul_reward": 600
    },
    "Bounding Demon":{
        "physical_def": 192,
        "magic_def": 135,
        "fire_def": 950,
        "HP": 1407,
        "soul_reward": 2000
    },
    "Large Mushroom":{
        "physical_def": (145, 156),
        "magic_def": (133, 159),
        "fire_def": (88, 93),
        "HP": (2376, 2483),
        "soul_reward": 1000
    },
}

COMMONS = len(common_enemies)
RARES = len(rare_enemies)
FEARSOMES = len(fearsome_enemies)

class Enemies(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

async def enemyPotentialSpawn(channel: discord.channel):
    spawn_chance = random.randint(1,300)
    if spawn_chance >=1 and spawn_chance <= 90:
        type_chance = random.randint(1,300)
        if type_chance > 0 and type_chance <= 250:
            await generateEnemy("common", channel)
        elif type_chance > 250 and type_chance <=290:
            await generateEnemy("rare", channel)
        else:
            await generateEnemy("fearsome", channel)
            

async def generateEnemy(rarity: str, channel: discord.channel):
    if rarity == "common":
        print("Common enemy spawned!")
        # Select a random common enemy
        enemy_name = random.choice(list(common_enemies.keys()))
        enemy_stats = common_enemies[enemy_name]

    elif rarity == "rare":
        print("Rare enemy spawned!")
        # Select a random rare enemy
        enemy_name = random.choice(list(rare_enemies.keys()))
        enemy_stats = rare_enemies[enemy_name]
    elif rarity == "fearsome":
        print("Fearsome enemy spawned!!!")
        # Select a random fearsome enemy
        enemy_name = random.choice(list(fearsome_enemies.keys()))
        enemy_stats = fearsome_enemies[enemy_name]
    else:
            print("Error while trying to make an enemy embed")
            return
    
    generated_stats={}

    for stat, value in enemy_stats.items():
        
        # Value of generated stat is within a range
        if isinstance(value, tuple):
            generated_stats[stat] = random.randint(*value)
        # Value of generated stat is a single, static value
        else:
            generated_stats[stat] = value

    # Assign values to generated stats
    physical_def = generated_stats["physical_def"]
    magic_def = generated_stats["magic_def"]
    fire_def = generated_stats["fire_def"]
    HP = generated_stats["HP"]
    soul_reward = generated_stats["soul_reward"]

    print(f"{physical_def}")    
    print(f"{magic_def}")   
    print(f"{fire_def}")
    print(f"{HP}")
    print(f"{soul_reward}")

    enemy_description = f"Physical Def = {physical_def}\nMagic Def = {magic_def}\nFire Def = {fire_def}"
    enemy_image = enemy_images.get(enemy_name)
    try:
        embed = discord.Embed(title=enemy_name, description= enemy_description,  color=discord.Color.red())
        print(f"Made embed title and description for {enemy_name}")
        embed.set_image(url=enemy_image)
        print("Set embed image")
        embed.add_field(name="HP remaining", value=HP, inline=True)
        print("Added embed field")
        print("reached end")
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Error while creating or sending embed: {e}")


# Add cog to the bot
async def setup(bot):
    await bot.add_cog(Enemies(bot))