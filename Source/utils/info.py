import discord, base64
from datetime import datetime
from rich import print

dt = datetime.now()

async def validate_token(token):
  import aiohttp
  headers = {
      "Content-Type": "application/json",
      "Authorization": token
  }
  async with aiohttp.ClientSession(headers = headers) as cs:
    async with cs.get('https://discordapp.com/api/v9/users/@me') as r:
      if r.status == 200:
        data = await r.json()
        return True, data["username"], data["id"]
      else:
        return False, None, None


async def validate_channel(token, ID):
  import asyncio, json, aiohttp
  if not isinstance(ID, int):
        try:
          ID = int(ID)
        except:
            return False
  headers = {
      "Content-Type": "application/json",
      "Authorization": token
  }
  async with aiohttp.ClientSession(headers = headers) as cs:
    async with cs.get(f'https://discord.com/api/v9/channels/{ID}') as r:
      """
      text = await r.text()
      
      print(json.dumps(data, indent = 4, sort_keys = True))
      """
      data = await r.json()
      if r.status == 200:
        if 775611298657468417 == int(data['guild_id']):
            return False
        return True
      else:
        return False

async def validate_hook(token, url):
  import aiohttp
  try:
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    async with aiohttp.ClientSession(headers = headers) as cs:
      async with cs.get(url) as r:
        if r.status == 200:
          return True
        else:
          return False
  except:
    return False