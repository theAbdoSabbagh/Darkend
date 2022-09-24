from rich import print
from discord.ext.commands import Bot

# Cooldowns

def commands_cooldown(bot : Bot, command : str):
  cooldowns = {
    "fish" : 40 if bot.internal['premium_status'] is False else 25,
    "hunt" : 40 if bot.internal['premium_status'] is False else 25,
    "dig" : 40 if bot.internal['premium_status'] is False else 25,
    "beg" : 45 if bot.internal['premium_status'] is False else 25,
    "deposit" : 60 if bot.internal['premium_status'] is False else 60,

    "crime" : 45 if bot.internal['premium_status'] is False else 15,
    "postmemes" : 50 if bot.internal['premium_status'] is False else 45,
    "search" : 30 if bot.internal['premium_status'] is False else 15,
    "trivia" : 5 if bot.internal['premium_status'] is False else 3,
    "highlow" : 30 if bot.internal['premium_status'] is False else 15,

    "slots" : 7  if bot.internal['premium_status'] is False else 3,
    "gamble" : 10  if bot.internal['premium_status'] is False else 5,
    "scratch" : 12  if bot.internal['premium_status'] is False else 5,
    "snakeeyes" : 12  if bot.internal['premium_status'] is False else 5,
  }
  
  return cooldowns[command]

def powerups_cooldown(name : str):
  cooldowns = {
    "pizza" : 3600,
    "horseshoe" : 900,
    "ammo" : 3600,
    "alcohol" : 36000,
    "apple" : 86400,
    "taco" : 86400,
    "fishingbait" : 3600,
    'whiskey' : 54000,
    'prestige' : 21600,
    'robbersmask' : 43200,
  }
  
  return cooldowns[name]

# Prices

def powerup_to_price(powerup : str):
  powerups = {
    # Can be bought
    "apple" : 8500,
    "horseshoe" : 75000,

    # Can't be bought
    "boots" : False,
    "alcohol" : False,
    "pizza" : False,
    "ammo" : False,
    "taco" :  False,
    "fishingbait" : False,
    'whiskey' : False,
    'prestige' : False,
    'robbersmask' :False,
  }
  for key, value in powerups.items():
    if powerup == key:
      return value

def sellable_item_prices(item : str = None):
  items = {'aplus': 3300000, 'ant': 11000, 'banhammer': 750000, 'beaker': 4275000, 'bean': 170000, 'boar': 30000, 'fish':
14500, 'cookie': 5000, 'corncob': 500000, 'corndog': 250000, 'deer': 65000, 'dragon': 250000, 'duck': 10000,
'ectoplasm': 1150000, 'energydrink': 3000000, 'exoticfish': 24000, 'fossil': 750000, 'bread': 12000, 'garbage': 5000,
'jellyfish': 50000, 'junk': 20000, 'kraken': 420000, 'ladybug': 20000, 'lawdegree': 6000000, 'legendaryfish': 200000,
'tree': 575000, 'memepills': 6500000, 'meteorite': 300000, 'note': 2000000, 'potato': 200000, 'rabbit': 9000,
'rarefish': 15000, 'seaweed': 5000, 'skunk': 8000, 'spider': 500000, 'starfragment': 2800000, 'stickbug': 15000,
'trash': 385000, 'vaccine': 6484000, 'worm': 9000}
  
  if item is None:
    return items

  return items[item]

# Other

def item_id(item : str):
  items = {
    "huntingrifle" : "huntingrifle",
    "fishingpole" : "fishingpole",
    "shovel" : "shovel",
    
    "A plus" : 'aplus', "Ant" : 'ant', "Ban Hammer" : 'banhammer',
    "Beaker of sus fluid" : 'beaker', "Bean" : 'bean', "Boar" : 'boar',
    "Common Fish" : 'fish', "Cookie" : 'cookie', "Corncob" : 'corncob',
    "Corndog" : 'corndog', "Deer" : 'deer', "Dragon" : 'dragon',
    "Duck" : 'duck', "Ectoplasm" : 'ectoplasm', "Energy Drink" : 'energydrink',
    "Exotic Fish" : 'exoticfish', "Fossil" : 'fossil', "Fresh Bread" : 'bread',
    "Garbage" : 'garbage', "Jelly Fish" : 'jellyfish', "Junk" : 'junk',
    "Kraken" : 'kraken', "Ladybug" : 'ladybug', "Law Degree" : 'lawdegree',
    "Legendary Fish" : 'legendaryfish', "Literally a Tree" : 'tree', "Meme pills" : 'memepills',
    "Meteorite" : 'meteorite', "Musical Note" : 'note', "Potato ☭" : 'potato',
    "Rabbit" : 'rabbit', "Rare Fish" : 'rarefish', "Seaweed" : 'seaweed',
    "Skunk" : 'skunk', "Spider" : 'spider', "Star Fragment" : 'starfragment',
    "Stickbug" : 'stickbug', "Trash" : 'trash', "Vaccine" : 'vaccine',
    "Worm" : 'worm',
  }

  return items[item]

def powerup_names(powerup : str):
  powerups = [
    "pizza",
    "apple",
    "alcohol",
    "horseshoe",
    "ammo",
    "taco",
    "fishingbait",
    "whiskey",
    "prestige",
    "robbersmask",
  ]

  if powerup in powerups:
    return True

  return False

def powerups_valid_name(powerup : str):
  powerups = {
    "pizza" : "Pizza",
    "apple" : "Apple",
    "alcohol" : "Alcohol",
    "horseshoe" : "Lucky Horseshoe",
    "ammo" : "Ammo",
    "taco" : "Crunchy Taco",
    "fishingbait" : "Fishing Bait",
    "whiskey" : "Whiskey",
    "prestige" : "Prestige Coin",
    "robbersmask" : "Robbers Mask",
    "boots": "Cowboy Boots"
  }

  return powerups[powerup]

def work_data(job_name : str):
  jobs = {
    "DiscordMod": {"name": "Discord Mod", "shifts_required": 0, "cooldown": 40, "unlock_requirement": 0, "salary": 10000},
    "Babysitter": {"name": "Babysitter", "shifts_required": 0, "cooldown": 40, "unlock_requirement": 0, "salary": 10500},
    "FastFoodCook": {"name": "Fast Food Cook", "shifts_required": 1, "cooldown": 43, "unlock_requirement": 0, "salary": 11111},
    "HouseWife": {"name": "House Wife", "shifts_required": 1, "cooldown": 43, "unlock_requirement": 0, "salary": 12000},
    "TwitchStreamer": {"name": "Twitch Streamer","shifts_required": 2,"cooldown": 46,"unlock_requirement": 20,"salary": 16000},
    "YouTuber": {"name": "YouTuber", "shifts_required": 2, "cooldown": 46, "unlock_requirement": 20, "salary": 17000},
    "ProfessionalHunter": {"name": "Professional Hunter", "shifts_required": 3, "cooldown": 49, "unlock_requirement": 30, "salary": 19000},
    "ProfessionalFisherman": {"name": "Professional Fisherman", "shifts_required": 3, "cooldown": 49, "unlock_requirement": 30, "salary": 20000},
    "Bartender": {"name": "Bartender", "shifts_required": 3, "cooldown": 49, "unlock_requirement": 40, "salary": 21000},
    "Robber": {"name": "Robber", "shifts_required": 3, "cooldown": 49, "unlock_requirement": 50, "salary": 22000},
    "PoliceOfficer": {"name": "Police Officer", "shifts_required": 3, "cooldown": 49, "unlock_requirement": 60, "salary": 23000},
    "Teacher": {"name": "Teacher", "shifts_required": 3, "cooldown": 49, "unlock_requirement": 80, "salary": 24000},
    "Musician": {"name": "Musician", "shifts_required": 3, "cooldown": 49, "unlock_requirement": 85, "salary": 25000},
    "ProGamer": {"name": "Pro Gamer", "shifts_required": 4, "cooldown": 52, "unlock_requirement": 100, "salary": 28000},
    "Manager": {"name": "Manager", "shifts_required": 4, "cooldown": 52, "unlock_requirement": 120, "salary": 29000},
    "Developer": {"name": "Developer", "shifts_required": 4, "cooldown": 52, "unlock_requirement": 150, "salary": 30000},
    "DayTrader": {"name": "Day Trader", "shifts_required": 5, "cooldown": 55, "unlock_requirement": 175, "salary": 35000},
    "SantaClaus": {"name": "Santa Claus", "shifts_required": 5, "cooldown": 55, "unlock_requirement": 185, "salary": 36000},
    "Politician": {"name": "Politician", "shifts_required": 5, "cooldown": 55, "unlock_requirement": 200, "salary": 37000},
    "Veterinarian": {"name": "Veterinarian", "shifts_required": 5, "cooldown": 55, "unlock_requirement": 200, "salary": 38000},
    "Pharmacist": {"name": "Pharmacist", "shifts_required": 5, "cooldown": 55, "unlock_requirement": 210, "salary": 39000},
    "DankMemerShopkeeper": {"name": "Dank Memer Shopkeeper", "shifts_required": 5, "cooldown": 55, "unlock_requirement": 225, "salary": 40000},
    "Lawyer": {"name": "Lawyer", "shifts_required": 6, "cooldown": 58, "unlock_requirement": 250, "salary": 45000},
    "Doctor": {"name": "Doctor", "shifts_required": 6, "cooldown": 58, "unlock_requirement": 280, "salary": 46000},
    "Scientist": {"name": "Scientist", "shifts_required": 6, "cooldown": 58, "unlock_requirement": 300, "salary": 47000},
    "Ghost": {"name": "Ghost", "shifts_required": 6, "cooldown": 58, "unlock_requirement": 350, "salary": 48000}
}

  return jobs[job_name]
