import discord
import random
import asyncio
import os

# Self Bot ke liye intents ki zaroorat nahi hoti, par safety ke liye default rakhe hain
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Client use kar rahe hain kyunki ye self bot ke saath stable rehta hai
bot = discord.Client(intents=intents)

# --- CONFIGURATION ---

GALLIES = [
    "sala", "bandar", "bewakoof", "chutiya", "gandgaa", 
    "tera baap", "macha", "kutta", "billi", "sher", 
    "aadmi", "jaantu", "pichkari", "bhenchod", "chod", 
    "nawabi", "kameena", "badmaash", "dhokebaaz", "jugaad"
]

# Pattern: Kitni baar copy karega, phir gali dega.
PATTERN = [1, 3, 5, 2, 4] 

# --- STATE ---
pattern_index = 0
messages_to_copy = PATTERN[0]
current_count = 0

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as: {bot.user}")
    # Self bot hone ki wajah se ye confirm karta hai ki wo user account hai
    print(f"User ID: {bot.user.id}")

@bot.event
async def on_message(message):
    global current_count, pattern_index, messages_to_copy

    # Agar message khud ka hai toh ignore kar
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
    # Ab hum 'SELF_TOKEN' padh rahe hain
    token = os.getenv('SELF_TOKEN')
    if not token:
        print("Error: SELF_TOKEN environment variable nahi mila!")
    else:
        # Self bot login ke liye 'login' method use karein, 'run' nahi
        # Kyunki 'run' bot ke liye optimized hai, 'login' user ke liye
        bot.run(token, log_level=30) # 30 means WARNING level, taaki spam na ho
