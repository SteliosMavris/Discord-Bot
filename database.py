import sqlite3
import discord

def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    database = sqlite3.connect('stats.db')
    cursor = database.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            userID INT PRIMARY KEY,
            level INT DEFAULT 1,
            souls INT DEFAULT 0,
            vitality INT DEFAULT 5,
            attunement INT DEFAULT 5,
            endurance INT DEFAULT 5,
            strength INT DEFAULT 5,
            dexterity INT DEFAULT 5,
            resistance INT DEFAULT 5,
            intelligence INT DEFAULT 5,
            faith INT DEFAULT 5,
            humanity INT DEFAULT 0
        )
    """)
    database.commit()
    database.close()

def add_user(user_id: int):
    """Add a new user to the database with default values."""
    database = sqlite3.connect('stats.db')
    cursor = database.cursor()

    # Insert the user with default values
    cursor.execute("""
        INSERT OR IGNORE INTO stats (userID)
        VALUES (?)
    """, (user_id,))
    database.commit()
    database.close()

def add_souls(user_id: int, reward: int):
    """Add souls to a user. If the user doesn't exist, add them first."""
    database = sqlite3.connect('stats.db')
    cursor = database.cursor()

    # Check if the user exists
    cursor.execute("SELECT 1 FROM stats WHERE userID = ?", (user_id,))
    user = cursor.fetchone()

    # Add the user if they don't exist
    if user is None:
        add_user(user_id)

    # Update the user's souls
    cursor.execute("""
        UPDATE stats
        SET souls = souls + ?
        WHERE userID = ?
    """, (reward, user_id))
    database.commit()
    database.close()

def upgrade(user_id: int, stats: str, interaction: discord.Interaction):
    souls = getSouls(user_id)
    level = getLevel(user_id)
    if level < 12:
        # For levels lower than 12 the requirement formula is y = 673 + current level * 17
        requirement = 673 + (level - 1) * 17
    else:
        # Compute required souls for next level using the equation from the darksouls wiki: y = 0.02x^3 + 3.06x^2 + 105.6x - 895
        # where x is the next level
        requirement = 0.02 * pow(level + 1, 3) + 3.06 * pow(level + 1, 2) + 105.6 * (level + 1) - 895
    if souls < requirement:
        interaction.response.send_message(f"You do not have enough souls to level up!\nSouls needed: {requirement - souls}")
        return
    database = sqlite3.connect('stats.db')
    cursor = database.cursor()
    query = f"""
        UPDATE stats
        SET {stats} = {stats} + ?,
            level = level + ?,
            souls = souls - ?
        WHERE userID = ?
    """
    cursor.execute(query, (1, 1, requirement, user_id))
    database.commit()
    database.close()
    
def get_user_stats(user_id: int):
    """Retrieve all data for a single user by their userID."""
    database = sqlite3.connect('stats.db')
    cursor = database.cursor()
    # Query the database for the user's details
    cursor.execute("SELECT * FROM stats WHERE userID = ?", (user_id,))
    user = cursor.fetchone()  # Fetch one row
    database.close()
    return user    

def isUserInDatabase(user_id: int):
    database = sqlite3.connect('stats.db')
    cursor = database.cursor()
    cursor.execute("""SELECT 1 FROM stats WHERE userID = ?""", (user_id,))
    user_exists = cursor.fetchone() is not None
    database.close()
    return user_exists

def getSouls(user_id: int):
    
    if not isUserInDatabase(user_id):
        raise ValueError(f"No entry found for userID: {user_id}")

    database = sqlite3.connect('stats.db')
    cursor = database.cursor()
    cursor.execute("SELECT souls FROM stats WHERE userID = ?", (user_id,))
    souls = cursor.fetchone()
    database.close()
        
    return int(souls[0])

def getLevel(user_id: int):
    
    if not isUserInDatabase(user_id):
        raise ValueError(f"No entry found for userID: {user_id}")
    
    database = sqlite3.connect('stats.db')
    cursor = database.cursor()
    cursor.execute("SELECT level FROM stats WHERE userID = ?", (user_id,))
    level = cursor.fetchone()
    database.close()

    return int(level[0])