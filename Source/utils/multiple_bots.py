import os, discord, random, asyncio

from discord.ext import commands
from colorama import init, Fore
from typing import Any, Optional

from utils.notifs import critical_messagebox_multi
from utils.useful import (custom_status, timer_to_seconds, success, error, darkend)

from utils.queued_functions import (presence_changer, log_hook, start_scraping_inventory, item_prices,
                                    update_data, command_executor, crash, error_log, fish_event, hunt_event)

from utils.alt_handler_assist import create_account_file, update_account_settings, get_account_settings
from utils.DankApi.commands_data import powerup_names, commands_cooldown

init(autoreset = True)

appdata = os.getenv('APPDATA')
directory = f"{appdata}\\Darkend v1"

async def start_bots(token, account_id, tray_icon, messenger):
  create_account_file(account_id)
  settings = get_account_settings(account_id)

  class DarkendBot(commands.Bot):
      PRE: tuple = ('lolol', 'lololol')
      def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=self.get_pre, self_bot = True, *args, **kwargs)
        self.settings = settings
        self.data = settings["data"]
        self.config = settings["config"]
        self.powerups = settings["powerups"]
        self.customization = settings["customization"]
        self.internal = {"autobuying_busy": False, "to_buy": [], "start_scraping": False,
        "scraper_working": False, "scraper_pages": False, "premium_status": False, "active_items": {},
        'waiting_presence': None, 'account_id': account_id, 'tray_icon': tray_icon, "interaction_is_active" : False,
        "started_at": 0, "error_hook": "fucking sikds"}
        self.messenger = messenger
        self.messenger.internal[account_id] = {"start_scraping": False, "scraper_pages": None, "scraper_working": False, "scraper_current_page": 0, "scraper_max_pages": 0, "scraper_last_page_item_amount": 0, "scraper_current_pages": 0,'autofarming': None, "profile_data": None, "crash": False}
        self.account_id = account_id
        self.last_ran = {'work':0, 'trivia' : 0, 'highlow' : 0, 'scratch' : 0, 'slots' : 0, 'gamble' : 0, 'snakeeyes' : 0, "deposit" : 0}
        self.last_used = {}

      async def get_pre(self, bot, message : discord.Message, raw_prefix : Optional[bool] = False):
          prefix = self.PRE
          return commands.when_mentioned_or(*prefix)(bot, message) if not raw_prefix else prefix

      async def on_error(self, event: str, *args: Any, **kwargs: Any):
        import traceback, sys
        (exc_type, exc, tb) = sys.exc_info()
        data = {
          "event": event,
          "traceback": "".join(traceback.format_exception(exc_type, exc, tb)),
        }
        await error_log(bot, data)

      async def get_balance_and_bank(self, bot, /, force = False):
        for i in range(5):
          channel = await self.return_channel(bot)
          if force is False:
            await self.send(bot, command = 'balance')
          else:
            await self.force_send(bot, command = 'balance')

          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.embeds is not None and m.interaction.user.id == bot.user.id, timeout = 5)
          if response is None:
            await asyncio.sleep(3.5)
            continue

          if "ongoing command running" in response.embeds[0].description.lower():
            return 0, 0
          
          try:
            balance = int(response.embeds[0].description.split('⏣ ')[1].replace(',', '').split('\n')[0])
            bank = int(response.embeds[0].description.split('⏣ ')[2].replace(',', '').split(' / ')[0].split('` ')[0])
            print(balance, bank)
          except:
            return 0, 0
          
          return balance, bank
      
        return 0, 0

      async def get_item_quantity(self, bot, item : str, retry: Optional[bool] = True):
        for i in range(5):
          channel = await self.return_channel(bot)
          await self.send(bot, command = 'item', item = item)
          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.embeds is not None and item in m.embeds[0].title and m.interaction.user.id == bot.user.id, timeout = 5)
          if response is None:
            await asyncio.sleep(3.5)
            continue

          try:
            quantity = int(''.join(c for c in response.embeds[0].title if c.isdigit()))
          except:
            return 0
          break

        return quantity

      async def withdraw(self, bot, /, amount : int, force = False):
        try:
          for i in range(5):
            channel = await self.return_channel(bot)
            if force is False:
              message = await self.send(bot, command = 'withdraw', amount = amount)
            else:
              message = await self.force_send(bot, command = 'withdraw', amount = amount)
            response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id and m.embeds is not None, timeout = 5)
            if response is None:
              await asyncio.sleep(5)
              continue

            if response.embeds[0].description is not None:
              if 'nothing to withdraw' in response.embeds[0].description.lower():
                return False
              if 'ongoing command running' in response.embeds[0].description.lower():
                return False

            if len(response.embeds[0].fields) != 0:
              if response.embeds[0].fields[0].name.lower() == 'withdrawn':
                return True
        except:
          return False
      
      async def buy_item(self, bot, /, item : str, force = False):
        for i in range(5):
          channel = await self.return_channel(bot)
          if force is False:
            await self.send(bot, command = "buy", item = item)
          else:
            await self.force_send(bot, command = "buy", item = item)
          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.embeds is not None and m.interaction.user.id == bot.user.id, timeout = 5)
          if response is None:
            await asyncio.sleep(5)
            continue

          try:
            if 'ongoing command' in response.embeds[0].description.lower():
              await self.wait_for_interaction_to_be_over(bot)
              continue
            if "you don't have enough" in response.embeds[0].description.lower():
              return False
            if "thanks for your purchase!" == response.embeds[0].footer.text.lower():
              return True
          except:
            return False

        return False

      async def click(self, response, components_num : int, children_num : int):
        for i in range(1000):
          try:
            await response.components[components_num].children[children_num].click(timeout = 0.5)
            if response.components[components_num].children is None:
              return True
            if response.components[components_num].children[children_num].disabled is True:
              return True
          except IndexError:
            return False
          except Exception as e:
            if 'COMPONENT_VALIDATION_FAILED' in str(e):
              return False
            error(f"{response.jump_url} || Error while trying to click the button: {e}")
            await asyncio.sleep(1)
            continue
          else:
            return True
        return False

      async def choose(self, response, components_num : int, children_num : int, option : int):
        for i in range(10):
          try:
            await response.components[components_num].children[children_num].choose(response.components[components_num].children[children_num].options[option])
          except Exception as e:
            if "400" in str(e):
              break
            error(e)
            await asyncio.sleep(0.5)
            continue
          break

        await asyncio.sleep(0.5)
        return True
      
      async def check_confirmations_setting(self, bot):
        while True:
          channel = await self.return_channel(bot)
          message = await self.send(bot, command = "settings")
          
          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.embeds is not None and m.interaction.user.id == bot.user.id, timeout = 5)
          if response is None:
            await asyncio.sleep(1.5)
            continue
          
          await self.choose(response, 0, 0, 3)
          value = True if response.components[1].children[1].disabled is True else False
          break
        print(value)
        return value

      async def check_if_powerup_is_active(self, bot, powerup):
        while True:
          channel = await self.return_channel(bot)
          
          await self.send(bot, command = 'profile')
          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.embeds is not None and m.interaction.user.id == bot.user.id and bot.user.name in m.embeds[0].title, timeout = 5)
          if response is None:
            await asyncio.sleep(5)
            continue

          break
        
        await self.choose(response, 0, 0, 1)
        
        if powerup.lower() in response.embeds[0].description.lower().replace('*', ''):
          return True
        
        return False

      async def cache_powerups(self, bot):
        while True:
          channel = await self.return_channel(bot)
          
          await self.send(bot, command = "profile")
          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.embeds is not None and m.interaction.user.id == bot.user.id and bot.user.name in m.embeds[0].title, timeout = 5)
          if response is None:
            await asyncio.sleep(5)
            continue

          break
        
        await self.choose(response, 0, 0, 1)
        
        powerup_state = False
        name = None
        if response.embeds[0].description == 'No active items right now':
          return False
        
        for line in response.embeds[0].description.split('\n'):
          seconds = timer_to_seconds(line.split('expires in ')[1])
          powerup_name = line.split('**')[1].split('**')[0].split(' ')
          for item in powerup_name:
            powerup_state = powerup_names(item.lower())
            if powerup_state is True:
              name = item
              break
          if powerup_state is True:
            self.internal['active_items'][name] = seconds
        
        return True

      async def use_powerup(self, bot, powerup):
        for i in range(5):
          channel = await self.return_channel(bot)
          message = await self.send(bot, command = "use", item = powerup)

          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id and m.interaction.id == message.id, timeout = 5)
          if response is None:
            await asyncio.sleep(5)
            continue

          if "you can't use this item" in response.embeds[0].description.lower():
            return {"status" : "active"}
          if "ongoing command running" in response.embeds[0].description.lower():
            return {"status" : "blocked"}
          if "you don't own" in response.embeds[0].description.lower():
            return {"status" : "doesn't own"}
          if "you have" in response.components[0].children[0].label.lower():
            return {"status" : "used"}
        
        return {"status" : "unknown"}
      
      async def send(self, bot, **kwargs):
        while True:
          if bot.messenger.internal[bot.user.id]['autofarming'] is False:
            await asyncio.sleep(0.5)
            continue
          
          channel = await self.return_channel(bot)
          command_name = kwargs['command']

          try:
            command = [command async for command in channel.slash_commands(query = str(command_name), limit = None) if str(command.name) == str(command_name) and command.application.id == 270904126974590976][0]
            message = await command(**kwargs)
          except discord.Forbidden:
            bot.messenger.internal[bot.user.id]['autofarming'] = False
            critical_messagebox_multi(bot.internal['tray_icon'], 'Missing Permissions', "Bot doesn't have the required permissions to send messages.\nAutofarming has been disabled.")
            return False
          except discord.HTTPException:
            error(f"Normal Send || HttpException")
            await asyncio.sleep(0.25)
            continue
          else:
            break
          
        return message

      async def force_send(self, bot, **kwargs):
        while True:
          channel = await self.return_channel(bot)
          command_name = kwargs['command']
          command : discord.SlashCommand
          try:
            command = [command async for command in channel.slash_commands(query = command_name, limit = None) if command.name == command_name and command.application.id == 270904126974590976][0]
            message = await command(**kwargs)
          except discord.Forbidden:
            bot.messenger.internal[bot.user.id]['autofarming'] = False
            critical_messagebox_multi(bot.internal['tray_icon'], 'Missing Permissions', "Bot doesn't have the required permissions to send messages.\nAutofarming has been disabled.")
            return False
          except discord.HTTPException:
            error(f"Force Send || HttpException")
            await asyncio.sleep(0.25)
            continue
          else:
            break
          
        return message

      async def sub_send(self, bot, command_name, sub_command_name, **kwargs):
        while True:
          channel = await self.return_channel(bot)
          command = [command async for command in channel.slash_commands(query = command_name, limit = None) if command.name == command_name and command.application.id == 270904126974590976][0]
          sub_command_index = 0
          for index, subcmd in enumerate(command.children):
            if subcmd.name.lower() == sub_command_name.lower():
              sub_command_index = index
              break
          try:
            interaction_response = await command.children[sub_command_index](**kwargs)
          except discord.Forbidden:
            bot.messenger.internal[bot.user.id]['autofarming'] = False
            critical_messagebox_multi(bot.internal['tray_icon'], 'Missing Permissions', "Bot doesn't have the required permissions to send messages.\nAutofarming has been disabled.")
            return False
          except discord.HTTPException:
            error(f"Sub Send || HttpException")
            await asyncio.sleep(0.25)
            continue
          else:
            break
        return interaction_response

      async def return_channel(self, bot : discord.Client):
        settings = get_account_settings(account_id)
        while True:
          try:
            channel = bot.get_channel(int(settings['data']['channel_id']))
          except discord.Forbidden:
            bot.messenger.internal[bot.user.id]['autofarming'] = False
            critical_messagebox_multi(bot.internal['tray_icon'], 'Missing Permissions', "The channel seems to be non-existent. If the channel does indeed exist, it means the bot doesn't have permissions to view it.")
            return False
          except Exception as e:
            if "none" in str(e).lower():
              channel = await self.fetch_channel(int(settings['data']['channel_id']))
              return channel

            await asyncio.sleep(0.25)
            continue
          
          return channel

      async def get_bot_data(self, bot):
        while True:
          channel = await self.return_channel(bot)
          
          message = await self.force_send(bot, command = "profile")
          response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.embeds is not None and m.interaction.user.id == bot.user.id and m.interaction.id == message.id, timeout = 5)
          if response is None:
            await asyncio.sleep(5)
            continue
          break

        try:
          if 'never used the bot' in response.embeds[0].description:
            data = {
              "level" : "N/A",
              "wallet" : "N/A",
              "bank" : "N/A",
              "net" : "N/A",
              "unique_items" : "N/A",
              "total_items" : "N/A",
              "total_commands": "N/A",
            }
            return data
        except:
          pass
        
        try:
          coins_field = response.embeds[0].fields[1].value
          items_field = response.embeds[0].fields[2].value
          to_replace = [',', '⏣', '%']
          
          for item in to_replace:
            coins_field = coins_field.replace(item, '')
            items_field = items_field.replace(item, '')

          level = response.embeds[0].fields[0].value.split('`')[1]
          total_commands = response.embeds[0].fields[3].value.split('\n')[0].split('`')[1]
          
          wallet = 0
          bank = 0
          net = 0
          unique_items = 0
          total_items = 0

          for line in coins_field.split('\n'):
            if 'wallet' in line.lower():
              wallet = line.split('`')[1].replace('⏣', '').replace(' ', '')
            if 'bank' in line.lower():
              bank = line.split('`')[1].replace('⏣', '').replace(' ', '')
            if 'net' in line.lower():
              net = line.split('`')[1].replace('⏣', '').replace(' ', '')
          
          for line in items_field.split('\n'):
            if 'unique' in line.lower():
              unique_items = line.split('`')[1].replace(' ', '')
            if 'total' in line.lower():
              total_items = line.split('`')[1].replace(' ', '')

          data = {
            "level" : level,
            "wallet" : wallet,
            "bank" : bank,
            "net" : net,
            "unique_items" : unique_items,
            "total_items" : total_items,
            "total_commands": total_commands,
          }

          # print(data)
          return data
        except:
          data = {
            "level" : "N/A",
            "wallet" : "N/A",
            "bank" : "N/A",
            "net" : "N/A",
            "unique_items" : "N/A",
            "total_items" : "N/A",
            "total_commands": "N/A",
          }
          return data

      async def safe_wait_for(self, bot, /, event : str, check, timeout : int = 60):
        try:
          response = await self.wait_for(event, check = check, timeout = timeout)
        except Exception as e:
          error(f'Safe wait for || {e.with_traceback()}')
          return None
        else:
          return response

      async def get_max_possible_job(self, bot):
        channel = await self.return_channel(bot)

        await self.sub_send(bot, 'work', 'list')
        response = await self.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction is not None and m.interaction.user.id == bot.user.id)
        if response is None:
          await asyncio.sleep(3.5)
          return None

        possible_jobs_amount = len([line for line in response.embeds[0].description.split('\n') if 'check' in line.lower()])
        job = None

        if possible_jobs_amount == 4:
          await asyncio.sleep(1.5)
          await self.click(response, 0, 2)

          while True:
            response = await self.safe_wait_for(bot, 'message_edit', check = lambda m, a: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction is not None and m.interaction.user.id == bot.user.id)
            
            if response is None:
              await asyncio.sleep(3.5)
              return None
            
            possible_jobs_amount = len([line for line in response[1].embeds[0].description.split('\n') if 'check' in line])
            if possible_jobs_amount == 0:
              break
            
            if possible_jobs_amount < 4:
              job = [line for line in response[1].embeds[0].description.split('\n') if 'check' in line][-1]
              await asyncio.sleep(2.5)
              return job.split('*')[2]
            
            if possible_jobs_amount == 4:
              await asyncio.sleep(2.5)
              await self.click(response[1], 0, 2)

          await asyncio.sleep(1.5)
          await self.click(response[1], 0, 1)
          response = await self.safe_wait_for(bot, 'message_edit', check = lambda m, a: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction is not None and m.interaction.user.id == bot.user.id)
          if response is None:
            await asyncio.sleep(3.5)
            return None
          job = [line for line in response[1].embeds[0].description.split('\n') if 'check' in line][-1]
          await asyncio.sleep(3.5)
          return job.split('*')[2]

        job = [line for line in response.embeds[0].description.split('\n') if 'check' in line][-1]
        await asyncio.sleep(3.5)
        return job.split('*')[2]

      async def apply_for_job(self, bot, job):
        while True:
          channel = await self.return_channel(bot)
          await self.sub_send(bot, 'work', 'apply', job = job)
          response = await self.safe_wait_for(bot, 'message', check = lambda m:m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction is not None and m.interaction.user.id == bot.user.id)
          if response is None:
            return None
          if 'recently resigned' in response.embeds[0].description.lower():
            await asyncio.sleep(3.5)
            return {"status" : "resigned"}
          if 'you are now working as' in response.embeds[0].description.lower():
            await asyncio.sleep(3.5)
            return {"status" : "success"}
          if 'you start now' in response.embeds[0].description.lower():
            await asyncio.sleep(3.5)
            return {"status" : "already working"}
          if 'were recently fired from your job' in response.embeds[0].description.lower():
            await asyncio.sleep(3.5)
            return {"status": "fired"}
          if 'ongoing' in response.embeds[0].description.lower():
            await self.wait_for_interaction_to_be_over(bot, response)
            continue
          if 'you need at least' in response.embeds[0].description.lower():
            await asyncio.sleep(3.5)
            return {"status": "not qualified"}

      async def wait_for_interaction_to_be_over(self, bot, /, response = None, timeout = 60):
        if response is not None:
          message_edit_response = await self.safe_wait_for(bot, 'message_edit', check = lambda m, a: m.interaction is not None and m.interaction.user.id == bot.user.id and m.id == response.id, timeout = timeout)
          try:
            if all([button.disabled for button in message_edit_response[1].components[0].children]) is True:
              return True
          except:
            return True
      
        message_edit_response = await self.safe_wait_for(bot, 'message_edit', check = lambda m, a: m.interaction is not None and m.interaction.user.id == bot.user.id and m.author.id == 270904126974590976, timeout = timeout)
        try:
          if all([button.disabled for button in message_edit_response[1].components[0].children]) is True:
            return True
        except:
          return True

      async def check_if_response_is_valid(self, /, response, check_components = False, check_buttons = False, components_num = 0):
        if 'default' and 'premium' and 'cooldown' in response.embeds[0].description.lower():
          return False
        if 'ongoing' in response.embeds[0].description.lower():
          return False
          
        if check_components is True:
          if response.components is None:
            return False
        if check_buttons is True:
          if response.components[components_num].children is None:
            return False

        return True

  bot = DarkendBot()

  @bot.listen('on_message')
  async def fish_event_sniper(message):
    if (message.author.id != 270904126974590976
    or message.embeds is None
    or message.interaction is None
    or message.interaction.user.id != bot.user.id):
      return

    try:
      if message.embeds[0].description is None:
        return
      if 'catch the fish' not in message.embeds[0].description.lower():
        return
    except IndexError:
      return
    except Exception as e:
      return error(f"Catch the fish || Error: {e}")
    
    await fish_event(bot, message)

  @bot.listen('on_message')
  async def hunt_event_sniper(message):
    if (message.author.id != 270904126974590976
    or message.embeds is None
    or message.interaction is None
    or message.interaction.user.id != bot.user.id):
      return

    try:
      if message.embeds[0].description is None:
        return
      if 'dodge the fireball' not in message.embeds[0].description.lower():
        return
    except IndexError:
      return
    except Exception as e:
      return error(f"Dodge The Fireball || Error: {e}")
    
    await hunt_event(bot, message)

  @bot.listen('on_message')
  async def other_event(message : discord.Message):
    if (message.author.id != 270904126974590976
    or message.embeds is None):
      return

    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      return
    
    if bot.customization['event_sniping'] is False:
      return

    try:
      if message.embeds[0].description is None:
        return
      if '**boss**' not in message.embeds[0].description.lower():
        return
    except Exception as e:
      return

    await log_hook(bot, f"Event Sniper — [Sniped \"{message.components[0].children[0].label}\" event]({message.jump_url}).")
    
    for i in range(10):
      if message.components[0].children[0].disabled is True:
        break
      await bot.click(message, 0, 0)

  @bot.listen('on_message')
  async def f_event(message : discord.Message):
    if (message.author.id != 270904126974590976
    or message.embeds is None):
      return
    
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      return
    if bot.customization['event_sniping'] is False:
      return

    try:
      if message.components[0].children[0].label.lower() != 'f':
        return
    except Exception as e:
      return

    await log_hook(bot, f"Event Sniper — [Sniped \"{message.components[0].children[0].label}\" event]({message.jump_url}).")
    
    for i in range(10):
      if message.components[0].children[0].disabled is True:
        break
      await bot.click(message, 0, 0)

  @bot.listen('on_message')
  async def alert(message):
    if message.author.id != 270904126974590976:
      return
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      return
    try:
      if bot.user.mentioned_in(message):
        if 'unread alert' in message.embeds[0].title.lower():
          await bot.force_send(bot, command = 'alert')
    except Exception as e:
      print(e)

  @bot.listen('on_message')
  async def ongoing(message):
    if message.author.id != 270904126974590976:
      return

    try:
      if 'ongoing command running' not in message.embeds[0].description.lower():
        return
    except:
      return

    bot.messenger.internal[bot.user.id]['autofarming'] = False
    print('Ongoing: Paused autofarming')
    await bot.wait_for_interaction_to_be_over(bot)
    bot.messenger.internal[bot.user.id]['autofarming'] = True
    print('Ongoing: Resumed autofarming')

  @bot.listen('on_message')
  async def captcha_solver_type_emoji_matcher(message):
    try:
      if message.author.id != 270904126974590976:
        return
      if message.embeds is None:
        return
      if message.embeds[0].title.lower() != 'captcha':
        return
      if 'matching image' not in message.embeds[0].description.lower():
        return
      if not bot.user.mentioned_in(message):
        return
    except:
      return
    
    try:
      emoji_link = message.embeds[0].image.url
      correct_button_index = None
      for index, button in enumerate(message.components[0].children):
        if button.emoji.url == emoji_link:
          correct_button_index = index
          print(f"Correct button is: {index+1}")
      await bot.click(message, 0, correct_button_index)
    except:
      pass

  @bot.listen('on_message')
  async def captcha_solver_type_pepe_emoji(message):
    try:
      if message.author.id != 270904126974590976:
        return
      if message.embeds is None:
        return
      if message.embeds[0].title.lower() != 'captcha':
        return
      if 'pepe' not in message.embeds[0].description.lower():
        return
      if not bot.user.mentioned_in(message):
        return
    except:
      return

    pepe_emojis = [
      819014822867894304, 796765883120353280,
      860602697942040596,  860602923665588284,
      860603013063507998, 936007340736536626,
      933194488241864704, 680105017532743700
    ]
    try:
      for component_index, component in enumerate(message.components):
        for button_index, button in enumerate(component.children):
          if button.emoji.id in pepe_emojis:
            await bot.click(message, component_index, button_index)
            await asyncio.sleep(0.5)
    except:
      pass

  @bot.listen('on_message')
  async def levelup(message):
    try:
      if settings['customization']['levelup_logging'] is False:
        return

      if (message.author.id != 270904126974590976
      or isinstance(message.channel, discord.DMChannel) is False
      or message.embeds is None
      or 'level up' in message.embeds[0].title.lower()):
        return

      level = int(message.embeds[0].description.split('level ')[1].split('!')[0].replace('*', ''))
      darkend(f"Reached level {level}.")
      if settings['customization']['levelup_logging'] is True:
        await log_hook(bot, f"Level Up — Reached level {level}.")
    except Exception as e:
      error(f"{bot.user} || Level Up || {e}")
      
  @bot.listen('on_message')
  async def lifesaver(message):
    if (message.author.id != 270904126974590976
    or isinstance(message.channel, discord.DMChannel) is False
    or message.embeds is None
    or message.embeds[0].title not in ['Your lifesaver protected you', 'You died', "Woah, you almost DIED!"]):
      return

    quote = "\""

    if message.embeds[0].title == 'You died':
      if settings['customization']['death_logging']:
        await log_hook(bot, f"Death — Bot just died. {'Initiating auto-buy process.' if settings['customization']['deathlifesaver'] is True else f'Please turn on {quote}Auto Lifesaver On Death{quote} in order for the bot to buy the powerup and re-use it.'}")
    
    elif message.embeds[0].title == 'Woah, you almost DIED!':
      if settings['customization']['death_logging']:
        await log_hook(bot, f"Death — Bot didn't die because this is the first time. {'Initiating auto-buy process.' if settings['customization']['deathlifesaver'] is True else f'Please turn on {quote}Auto Lifesaver On Death{quote} in order for the bot to buy the powerup and re-use it.'}")

    else:
      try:
        lifesavers = int(message.embeds[0].description.split('(You have ')[1].split(' left)')[0])
      except:
        darkend("Failed to check Lifesaver amount.")
        await log_hook(bot, f"Auto LifeSaver On Death — Failed to check the lifesavers amount.")
        return

      darkend(f"Lifesaver protected the bot from dying. `{lifesavers}` Lifesavers left.")
      if settings['customization']['death_logging']:
        await log_hook(bot, f"Death — Lifesaver protected the bot from dying. `{lifesavers}` Lifesavers left.")
      
      if lifesavers > 1:
        return
    
      if settings['customization']['death_logging']:
        await log_hook(bot, f"Death — Lifesaver protected the bot from dying. `{lifesavers}` Lifesavers left. {'Initiating auto-buy process.' if settings['customization']['deathlifesaver'] is True else f'Please turn on {quote}Auto Lifesaver On Death{quote} in order for the bot to buy the powerup and re-use it.'}")
    
    if settings['customization']['deathlifesaver'] is False:
      return
    
    # Make it false, make it true after it buys
    bot.messenger.internal[bot.user.id]['autofarming'] = False
    await bot.wait_for_interaction_to_be_over(bot, timeout = 5)

    balance, bank = await bot.get_balance_and_bank(bot, force = True)
    darkend(f'Balance: {balance}\nBank: {bank}')

    needed_money = 85000 - balance if 85000 - balance > 0 else 85000
    bank_money_state = bank > needed_money

    if balance >= 85000:
      success(f'Balance is enough to buy a Lifesaver.')
      buy_state = await bot.buy_item(bot, 'Life Saver', force = True)
      if buy_state is False:
        darkend("Failed to buy a Lifesaver.")
        await log_hook(bot, f"Auto LifeSaver On Death — Failed to buy a lifesaver.")
        bot.messenger.internal[bot.user.id]['autofarming'] = True
        return
      success(f'Bought a Lifesaver.')
      await log_hook(bot, f"Auto LifeSaver On Death — Bought a lifesaver.")

    if bank_money_state is True:
      if settings['customization']['withdraw'] is False:
        error(f'Balance is not enough to buy a Lifesaver.')
        bot.messenger.internal[bot.user.id]['autofarming'] = True
        return await log_hook(bot, f"Auto LifeSaver On Death — Balance is not enough to buy a `Lifesaver`, please enable \"Auto Withdraw\" in order for the item to be bought.")

      withdraw_state = await bot.withdraw(bot, needed_money, force = True)

      if withdraw_state is False:
        darkend(f"Bot cannot withdraw {needed_money}.")
        await log_hook(bot, f"Auto LifeSaver On Death — Couldn't withdraw {needed_money} to buy a `Lifesaver`.")
        
      darkend(f"Withdrawn {needed_money}.")
      buy_state = await bot.buy_item(bot, 'Life Saver', force = True)
      if buy_state is False:
        darkend("Failed to buy a Lifesaver.")
        await log_hook(bot, f"Auto LifeSaver On Death — Failed to buy a lifesaver.")
        bot.messenger.internal[bot.user.id]['autofarming'] = True
        return
      await log_hook(bot, f"Auto LifeSaver On Death — Bought a `Lifesaver`.")

    if bank_money_state is False:
      await log_hook(bot, f"Auto LifeSaver On Death — Balance & Bank are not enough to purchase a `lifesaver`. Skipping the process of buying the item.")
      
    bot.messenger.internal[bot.user.id]['autofarming'] = True

  @bot.listen('on_ready')
  async def botready():
    import time
    bot.messenger.internal[bot.user.id]['autofarming'] = True
    bot.internal['started_at'] = time.time()
    try:
      await bot.change_presence(status = custom_status(bot))
    except:
      pass
    print('Starting autofarm...')
    if settings['customization']['autofarm_logging'] is True:
      await log_hook(bot, 'Autofarm State — Started Autofarming.')
    
    # Testing
    # await bot.get_bot_data(bot)

    # Crashing
    bot.loop.create_task(crash(bot))

    # Real time settings
    bot.loop.create_task(update_data(bot))

    # Other utilities
    bot.loop.create_task(start_scraping_inventory(bot))
    # bot.loop.create_task(cache_powerups_task(bot))

    # Presence Changer
    bot.loop.create_task(presence_changer(bot))

    bot.loop.create_task(command_executor(bot))

  # bot.run(token)
  await bot.start(token)

def between_callback(token, account_id, tray_icon, messenger):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(start_bots(token, account_id, tray_icon, messenger))
  loop.close()