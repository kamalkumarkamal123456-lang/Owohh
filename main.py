import discord
import random
import asyncio
import os
import time

# Discord Intents Settings
# Ye zaroori hai taaki bot messages padh sake
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Bot Initialize
bot = discord.Bot(intents=intents)

# --- CONFIGURATION AREA ---

# 1. Galiyan ki list (Customize kar sakte ho)
GALLIES = [
    "sala", "bandar", "bewakoof", "chutiya", "gandgaa", 
    "tera baap", "macha", "kutta", "billi", "sher", 
    "aadmi", "jaantu", "pichkari", "bhenchod", "chod", 
    "nawabi", "kameena", "badmaash", "dhokebaaz", "jugaad"
]

# 2. Pattern Logic
# Iska matlab: 
# Pehle 1 message copy karo -> Fir 1 gali bolo
# Fir 3 messages copy karo -> Fir 1 gali bolo
# Fir 5 messages copy karo -> Fir 1 gali bolo
# Fir 2 messages copy karo -> Fir 1 gali bolo
# Fir 4 messages copy karo -> Fir 1 gali bolo
# Phir loop wapas pehle pattern (1) par aayega.
PATTERN = [1, 3, 5, 2, 4] 

# --- INTERNAL STATE (No Database) ---
pattern_index = 0
messages_to_copy = PATTERN[0]
current_count = 0

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as: {bot.user}")
    print(f"Target Server: {bot.guilds[0].name if bot.guilds else 'N/A'}")

@bot.event
async def on_message(message):
    global current_count, pattern_index, messages_to_copy

    # 1. Agar khud ka message hai toh copy mat karo (Infinite loop se bachne ke liye)
    if message.author == bot.user:
        return

    # 2. Original Message Copy Karna
    # Thoda random delay taaki natural lage aur spam detect na ho
    delay = random.uniform(0.5, 1.2)
    await asyncio.sleep(delay)
    
    await message.channel.send(message.content)
    
    # Count badhao
    current_count += 1
    
    # 3. Check karo ki kya ab Gali bhejne ka time hai?
    if current_count >= messages_to_copy:
        # Gali Select karo
        random_gali = random.choice(GALLIES)
        
        # Gali bhejne se pehle thoda delay
        await asyncio.sleep(random.uniform(0.1, 0.4))
        
        # Gali bhejo
        await message.channel.send(random_gali)
        
        # Pattern Advance Karna
        pattern_index += 1
        
        # Agar pattern khatam ho gaya hai, toh wapas shuru se shuru karo
        if pattern_index < len(PATTERN):
            messages_to_copy = PATTERN[pattern_index]
        else:
            pattern_index = 0
            messages_to_copy = PATTERN[0]
        
        # Count Reset karo next round ke liye
        current_count = 0

# Bot Run Karna
if __name__ == "__main__":
    # Token environment variable se lo
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("Error: BOT_TOKEN environment variable nahi mila!")
    else:
        bot.run(token)
