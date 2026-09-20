import discord
import random
import asyncio
import os

# Discord Intents Settings
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Bot Initialize (Client use kiya hai kyunki prefix nahi chahiye)
bot = discord.Client(intents=intents)

# --- CONFIGURATION AREA ---

GALLIES = [
    "sala", "bandar", "bewakoof", "chutiya", "gandgaa", 
    "tera baap", "macha", "kutta", "billi", "sher", 
    "aadmi", "jaantu", "pichkari", "bhenchod", "chod", 
    "nawabi", "kameena", "badmaash", "dhokebaaz", "jugaad"
]

# Pattern: Kitni baar copy karega, phir gali dega. 
# Example: [1, 3, 5] = 1 msg copy, phir 3 msg copy, phir 5 msg copy, phir gali.
PATTERN = [1, 3, 5, 2, 4] 

# --- INTERNAL STATE ---
pattern_index = 0
messages_to_copy = PATTERN[0]
current_count = 0

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as: {bot.user}")
    print(f"Connected to server: {bot.guilds[0].name if bot.guilds else 'No servers'}")

@bot.event
async def on_message(message):
    global current_count, pattern_index, messages_to_copy

    # Bot khud ka message copy na kare
    if message.author == bot.user:
        return

    # Original Message Copy Karna
    delay = random.uniform(0.5, 1.2)
    await asyncio.sleep(delay)
    
    await message.channel.send(message.content)
    
    current_count += 1
    
    if current_count >= messages_to_copy:
        random_gali = random.choice(GALLIES)
        await asyncio.sleep(random.uniform(0.1, 0.4))
        await message.channel.send(random_gali)
        
        pattern_index += 1
        
        if pattern_index < len(PATTERN):
            messages_to_copy = PATTERN[pattern_index]
        else:
            pattern_index = 0
            messages_to_copy = PATTERN[0]
        
        current_count = 0

if __name__ == "__main__":
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("Error: BOT_TOKEN environment variable nahi mila!")
    else:
        bot.run(token)
