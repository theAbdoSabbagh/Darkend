from logging import Logger
import os, discord, time
import traceback

from utils.useful import custom_status, success, error, darkend, misc
from utils.alt_handler_assist import get_account_settings, update_account_settings
from utils.DankApi.commands_data import commands_cooldown, powerups_cooldown, powerup_to_price, powerups_valid_name
from colorama import init, Fore
from rich import print

init(autoreset = True)

appdata = os.getenv('APPDATA')
directory = f"{appdata}\\Darkend v1"
empty_inventory_text = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Century Gothic'; font-size:13px; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">The inventory is empty.</p></body></html>"""

# Commands

async def auto_trivia(bot, sleep_time):
  from utils.useful import log_trivia
  import asyncio, random, json

  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break

  if time.time() - bot.last_ran['trivia'] <= sleep_time:
    return True

  channel = await bot.return_channel(bot)
  await bot.send(bot, command = 'trivia')
  click_state = False
  bot.last_ran['trivia'] = time.time()
  
  message_response = await bot.safe_wait_for(bot, 'message', check = lambda m:  m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id , timeout = 5)
  if message_response is None:
    error(f"Couldn't wait for message in command 'Trivia'")
    bot.last_ran['trivia'] = time.time()
    return True

  bot.last_ran['trivia'] = time.time()
  validation_state = await bot.check_if_response_is_valid(message_response, check_buttons = True, components_num = 0)
  if validation_state is False:
    error('Trivia || Validation state is False')
    return True
  
  try:
    with open(f"{directory}\\trivia.json", "r+") as trivia_file:
        answers = json.loads(trivia_file.read())
    question = message_response.embeds[0].description.split("\n")[0].replace("*", "")
    chosen = answers[question]
    for index, possible_answer in enumerate(message_response.components[0].children):
      if possible_answer.label == chosen:
        click_state = await bot.click(message_response, 0, index)      
  except:
    click_state = await bot.click(message_response, 0, 0)
    for button in message_response.components[0].children:
      if button.style == discord.ButtonStyle.success:
        answer = button.label
    try:
      await log_trivia(question, answer)
    except:
      pass

  if click_state is False:
    error('Trivia || Failed to click button.')
    await bot.wait_for_interaction_to_be_over(bot, message_response)
    bot.last_ran['trivia'] = time.time()
    success('Trivia || Finished waiting for interaction to be over.')
    
  return True

async def auto_highlow(bot, sleep_time):
  import asyncio, random
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      print('its false')
      await asyncio.sleep(0.5)
      continue
    break

  if time.time() - bot.last_ran['highlow'] <= sleep_time:
    return True

  channel = await bot.return_channel(bot)
  message = await bot.send(bot, command = "highlow")
  bot.last_ran['highlow'] = time.time()
  
  response = await bot.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id , timeout = 5)
  if response is None:
    error(f"Couldn't wait for message in command 'Highlow'")
    bot.last_ran['highlow'] = time.time()
    return True
  
  bot.last_ran['highlow'] = time.time()
  validation_state = await bot.check_if_response_is_valid(response, check_buttons = True, components_num = 0)
  if validation_state is False:
    error('Highlow || Validation state is False')
    return True

  try:
    number = int(response.embeds[0].description.split('\n')[1].split('than ')[1].replace('*', '').split('.')[0].replace('?', ''))
    if number > 50:
      click_state = await bot.click(response, 0, 0)
    else:
      click_state = await bot.click(response, 0, 2)
  except:
    click_state = await bot.click(response, 0, 2)
  
  if click_state is False:
    # This is so the interaction is finished
    await bot.wait_for_interaction_to_be_over(bot, response)
    bot.last_ran['highlow'] = time.time()
    success('Highlow || Finished waiting for interaction to be over.')

  return True

async def auto_scratch(bot, sleep_time):
  import asyncio, random
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break

  if time.time() - bot.last_ran['scratch'] <= sleep_time:
    return True
  
  bet = bot.config['scratch_bet']
  channel = await bot.return_channel(bot)
  await bot.send(bot, command = "scratch", bet = bet)
  bot.last_ran['scratch'] = time.time()

  message_response = await bot.safe_wait_for(bot, 'message', check =  lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id , timeout = 5)
  if message_response is None:
    bot.last_ran['scratch'] = time.time()
    return True

  bot.last_ran['scratch'] = time.time()
  validation_state = await bot.check_if_response_is_valid(message_response, check_buttons = True, components_num = 0)
  if validation_state is False:
    error('Scratch || Validation state is False')
    return True
  
  if 'you only have' in message_response.embeds[0].description.lower():
    
    if bot.customization['withdraw'] is False:
      darkend("Bot doesn't have enough balance & bank to run the command `scratch`. The bot will wait for a few minutes before trying again.")
      await log_hook(bot, "Auto Scratch — Bot doesn't have enough balance & bank to run the command `scratch`. The bot will wait for a few minutes before trying again.")
      await asyncio.sleep(300)
      return True

    withdraw_state = await bot.withdraw(bot, bet)

    if withdraw_state is False:
      darkend("Bot doesn't have enough balance & bank to run the command `scratch`. The bot will wait for a few minutes before trying again.")
      await log_hook(bot, "Auto Scratch — Bot doesn't have enough balance & bank to run the command `scratch`. The bot will wait for a few minutes before trying again.")
      await asyncio.sleep(300)
      return True

  if bot.user.name in message_response.embeds[0].author.name:
    for i in range(3):
      random_button = random.randrange(2)
      click_state = await bot.click(message_response, i, random_button)
      await asyncio.sleep(1.5)

  if click_state is False:
    error('Scratch || Failed to click button.')
    await bot.wait_for_interaction_to_be_over(bot, message_response)
    bot.last_ran['scratch'] = time.time()
    success('Scratch || Finished waiting for interaction to be over.')

  return True

async def button_tasks(bot, action, state, buttons_count):
  import asyncio, random
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break

  if bot.config[state] is False:
    return True
  if action not in bot.last_ran:
    bot.last_ran[action] = 0
  sleep_time = commands_cooldown(bot, action)
  if time.time() - bot.last_ran[action] <= sleep_time:
    return True
 
  click_state = True
  channel = await bot.return_channel(bot)
  message = await bot.send(bot, command = action)
  bot.last_ran[action] = time.time()

  message_response = await bot.safe_wait_for(bot, 'message', check =  lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id , timeout = 5)
  if message_response is None:
    bot.last_ran[action] = time.time()
    return True

  bot.last_ran[action] = time.time()
  validation_state = await bot.check_if_response_is_valid(message_response, check_buttons = True, components_num = 0)
  if validation_state is False:
    error(f'{action} || Validation state is False')
    return True

  if action.lower() in ['search', 'scout']:
    for index, button in enumerate(message_response.components[0].children):
      if str(button.label) in bot.config['search_places']:
        click_state = await bot.click(message_response, 0, index)
        break

      random_number = random.randrange(int(buttons_count))
      click_state = await bot.click(message_response, 0, random_number)
      break

  elif action.lower() == 'crime':
    for index, button in enumerate(message_response.components[0].children):
      if str(button.label) in bot.config['crime_actions']:
        click_state = await bot.click(message_response, 0, index)
        break

      random_number = random.randrange(int(buttons_count))
      click_state = await bot.click(message_response, 0, random_number)
      break
  
  else:
    random_number = random.randrange(int(buttons_count))
    click_state = await bot.click(message_response, 0, random_number)

  if click_state is False:
    error(f'{action.title()} || Failed to click button.')
    await bot.wait_for_interaction_to_be_over(bot, message_response)
    bot.last_ran[action] = time.time()
    success(f'{action.title()} || Finished waiting for interaction to be over.')

  return True

async def raw_tasks(bot, action, state):
  import asyncio
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break
    
  if bot.config[state] is False:
    return True
  if action not in bot.last_ran:
    bot.last_ran[action] = 0
  sleep_time = commands_cooldown(bot, action)
  if time.time() - bot.last_ran[action] <= sleep_time:
    return True

  channel = await bot.return_channel(bot)
  message = await bot.send(bot, command = action)
  bot.last_ran[action] = time.time()
    
  response = await bot.safe_wait_for(bot, 'message', check = lambda m:  m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id , timeout = 5)
  if response is None:
    bot.last_ran[action] = time.time()
    return True
  
  bot.last_ran[action] = time.time()
  validation_state = await bot.check_if_response_is_valid(response)
  if validation_state is False:
    error(f'{action} || Validation state is False')
    return True

  if 'catch the fish' in response.embeds[0].description.lower():
    state = await fish_event(bot, message)

  if ("you don't have a" not in response.embeds[0].description.lower()
  or bot.customization['autotool'] is False):
    bot.last_ran[action] = time.time()
    return True

  temp = response.embeds[0].description.split(",")[0].split("a ")[1].title()  
  error(f"Bot doesn't have a {temp}. Pausing the command {action} until successful purchase.")
  buying_state = await auto_buy_tool(bot, temp)
  bot.last_ran[action] = time.time()
  return True

async def gamble_tasks(bot, action, state):
  import asyncio
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break
    
  if bot.config[state] is False:
    return True
  sleep_time = commands_cooldown(bot, action)
  if time.time() - bot.last_ran[action] <= sleep_time:
    return True

  bet = bot.config[f"{state}_bet"]
  
  channel = await bot.return_channel(bot)
  message = await bot.send(bot, command = action, bet = bet)
  bot.last_ran[action] = time.time()
  
  response = await bot.safe_wait_for(bot, 'message', check =  lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id , timeout = 5)
  if response is None:
    bot.last_ran[action] = time.time()
    return True

  bot.last_ran[action] = time.time()
  validation_state = await bot.check_if_response_is_valid(response)
  if validation_state is False:
    error(f'{action} || Validation state is False')
    return True

  if 'you only have' in response.embeds[0].description.lower():
    if bot.customization['withdraw'] is False:
      darkend(f"Bot doesn't have enough balance & bank to run the command `{action.title()}`. Waiting for 5 minutes.")
      await log_hook(bot, f"Auto {action.title()} — Bot doesn't have enough balance & bank to run the command `{action.title()}`. Waiting for **5** minutes.")
      bot.last_ran[action] = time.time() + 300
      return True
      
    withdraw_state = await bot.withdraw(bot, bet)

    if withdraw_state is False:
      darkend(f"Bot doesn't have enough balance & bank to run the command `{action.title()}`. Waiting for 5 minutes.")
      await log_hook(bot, f"Auto {action.title()} — Bot doesn't have enough balance & bank to run the command `{action.title()}`. Waiting for **5** minutes.")
      bot.last_ran[action] = time.time() + 300
      return True
    
  bot.last_ran[action] = time.time()
  return True

async def auto_deposit(bot, sleep_time):
  import asyncio
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      print('its false')
      await asyncio.sleep(0.5)
      continue
    break

  if bot.config['auto_dep'] is False:
    return True
  if time.time() - bot.last_ran['deposit'] <= sleep_time:
    return True

  channel = await bot.return_channel(bot)
  message = await bot.send(bot, command = "deposit", amount = "max")
  bot.last_ran['deposit'] = time.time()
  
  response = await bot.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id , timeout = 5)
  if response is None:
    bot.last_ran['deposit'] = time.time()
    return True
  
  bot.last_ran['deposit'] = time.time()
  return True

async def auto_work(bot):
  import asyncio, random
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break

  if bot.config['work'] is False:
    return True
  if time.time() - bot.last_ran['work'] <= 3700:
    return True

  channel = await bot.return_channel(bot)
  await bot.sub_send(bot, 'work', 'shift')
  response = await bot.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction is not None and m.interaction.user.id == bot.user.id)
  
  if response is None:
    await asyncio.sleep(3.5)
    return True
  
  if ("were recently fired from your job" in response.embeds[0].description.lower()
  or "your boss decided to fire you" in response.embeds[0].description.lower()):
    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Bot is fired. Turning auto work off.")
    bot.settings['config']['work'] = False
    update_account_settings(bot.user.id, bot.settings)
    return True

  if 'recently resigned' in response.embeds[0].description.lower():
    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Bot will wait for default resign cooldown to be over.")
    bot.last_ran['work'] = time.time() + 10900
    return True

  if 'ongoing' in response.embeds[0].description.lower():
    await bot.wait_for_interaction_to_be_over(bot, response)
    success(f'Work || Finished waiting for interaction to be over.')

  while True:
    if "currently have a job to work at" in response.embeds[0].description.lower():
      await asyncio.sleep(3.5)
      job = bot.config['preferred_job']
      if bot.config['preferred_job'] == 'Automatic':
        job = await bot.get_max_possible_job(bot) 
      status = await bot.apply_for_job(bot, job)

      if status['status'] == 'resigned':
        if bot.customization['work_logging'] is True:
          await log_hook(bot, "Auto Work — Bot will wait for default resign cooldown to be over.")
        bot.last_ran['work'] = time.time() + 10900
        return True
      
      elif status['status'] == 'success':
        await asyncio.sleep(3.5)
        await bot.sub_send(bot, 'work', 'shift')
        response = await bot.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction is not None and m.interaction.user.id == bot.user.id)
        if response is None:
          await asyncio.sleep(3.5)
          return True
        break
      
      elif status['status'] == 'already working':
        break
      
      elif status['status'] == 'fired':
        if bot.customization['work_logging'] is True:
          await log_hook(bot, "Auto Work — Bot is fired. Turning auto work off.")
        bot.settings['config']['work'] = False
        update_account_settings(bot.user.id, bot.settings)
        return True
      
      elif status['status'] == 'not qualified':
        if bot.customization['work_logging'] is True:
          await log_hook(bot, f"Auto Work — Can't apply for `{job}` because the bot isn't qualified for it.")
        error(f"Can't apply for `{job}` because the bot isn't qualified for it.")
        await asyncio.sleep(3.5)
        job = await bot.get_max_possible_job(bot) 
        status = await bot.apply_for_job(bot, job)
        if status['status'] == 'success':
          await bot.sub_send(bot, 'work', 'shift')
          response = await bot.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction is not None and m.interaction.user.id == bot.user.id)
          if response is None:
            return True
          break
        else:
          if bot.customization['work_logging'] is True:
            await log_hook(bot, f"Auto Work — Failed to do anything. The bot will wait for an hour before re-trying.")
          error("Failed to do anything. The bot will wait for an hour before re-trying.")
          bot.last_ran['work'] = time.time()
          return True
      else:
        if bot.customization['work_logging'] is True:
          await log_hook(bot, "Auto Work — Bot will wait for default cooldown to be over.")
        bot.last_ran['work'] = time.time()
        return True
    
    else:
      break

  if "you need to wait" in response.embeds[0].description.lower():
    darkend("u need to wait")
    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Bot will wait for defatul cooldown to be over.")
    bot.last_ran['work'] = time.time()
    return True

  embed_content = response.embeds[0].description.lower()
  button : discord.Button
  middle = "<:emptyspace:827651824739156030>"
  right = "<:emptyspace:827651824739156030><:emptyspace:827651824739156030>"

  left_index = 0
  middle_index = 1
  right_index = 2

  bot.last_ran['work'] = time.time()

  if 'look at the emoji closely' in embed_content:
    emoji = embed_content.split('\n')[1].replace(' ', '').strip()
    message_edit_response = await bot.safe_wait_for(bot, 'message_edit', check = lambda m, a: a.interaction is not None and a.interaction.user.id == bot.user.id)

    if message_edit_response is None:
      await asyncio.sleep(3.5)
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Look At The Emojis Closely\" mini-game due to Dank Memer lag.")
      return error("Failed to wait for \"message edit\" event.")

    click_state = False
    for index, button in enumerate(message_edit_response[1].components[0].children):
      if str(button.emoji).replace(' ', '').strip() == emoji:
        click_state = await bot.click(message_edit_response[1], 0, index)
        break
    
    for index, button in enumerate(message_edit_response[1].components[1].children):
      if str(button.emoji).replace(' ', '').strip() == emoji:
        click_state = await bot.click(message_edit_response[1], 1, index)
        break

    if click_state is False:
      error('Work || Failed to click button.')
      await bot.wait_for_interaction_to_be_over(bot, message_edit_response[1])
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Look At The Emojis Closely\" mini-game because of Discord button-clicking ratelimit.")
      success('Work || Finished waiting for interaction to be over.')
      return

    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Successfully completed the \"Look At The Emojis Closely\" mini-game.")
    success("Successfully completed the \"Look At The Emojis Closely\" mini-game.")
    return
    
  elif 'remember words order' in embed_content:
    words_in_order = [item.lower() for item in embed_content.replace('`', '').split('\n')[1:]]
    message_edit_response = await bot.safe_wait_for(bot, 'message_edit', check = lambda m, a: a.interaction is not None and a.interaction.user.id == bot.user.id)
    
    if message_edit_response is None:
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Remember Words Order\" mini-game due to Dank Memer lag.")
      return error("Failed to wait for \"message edit\" event.")
    
    click_state = False
    for item in words_in_order:
      for index, button in enumerate(message_edit_response[1].components[0].children):
        if button.label.lower() == item:
          click_state = await bot.click(message_edit_response[1], 0, index)
          await asyncio.sleep(0.5)
          break
        
    if click_state is False:
      error('Work || Failed to click button.')
      await bot.wait_for_interaction_to_be_over(bot, message_edit_response[1])
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Remember Words Order\" mini-game because of Discord button-clicking ratelimit.")
      success('Work || Finished waiting for interaction to be over.')
      return

    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Successfully completed the \"Remember words order\" mini-game.")
    
    success("Successfully completed the \"Remember words order\" mini-game.")
    return

  elif 'dunk the ball' in embed_content:
    message_edit_response = await bot.safe_wait_for(bot, 'message_edit', check = lambda m, a: a.interaction is not None and a.interaction.user.id == bot.user.id)

    if message_edit_response is None:
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Dunk The Ball\" mini-game due to Dank Memer lag.")
      return error("Failed to wait for \"message edit\" event.")
    
    click_state = False
    embed_content = message_edit_response[1].embeds[0].description.lower()
    if embed_content.split('\n')[2].startswith(middle):
      click_state = await bot.click(response, 0, middle_index)
    elif embed_content.split('\n')[2].startswith(right):
      click_state = await bot.click(response, 0, right_index)
    else:
      click_state = await bot.click(response, 0, left_index)
    
    if click_state is False:
      error('Work || Failed to click button.')
      await bot.wait_for_interaction_to_be_over(bot, message_edit_response[1])
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Dunk The Ball\" mini-game because of Discord button-clicking ratelimit.")
      success('Work || Finished waiting for interaction to be over.')
      return

    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Successfully completed the \"Dunk The Ball\" mini-game.")

    success("Successfully completed the \"Dunk The Ball\" mini-game.")
    return

  elif 'hit the ball' in embed_content:
    message_edit_response = await bot.safe_wait_for(bot, 'message_edit', check = lambda m, a: m.interaction is not None and m.interaction.user.id == bot.user.id and m.id == response.id)
    
    if message_edit_response is None:
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Hit The Ball\" mini-game due to Dank Memer lag.")
      return error("Failed to wait for \"message edit\" event.")
    
    click_state = False
    embed_content = message_edit_response[1].embeds[0].description.lower()
    if embed_content.split('\n')[2].startswith(middle):
      click_state = await bot.click(response, 0 , random.choice([left_index, right_index]))
    elif embed_content.split('\n')[2].startswith(right):
      click_state = await bot.click(response, 0 , random.choice([left_index, middle_index]))
    else:
      click_state = await bot.click(response, 0 , random.choice([middle_index, right_index]))

    if click_state is False:
      error('Work || Failed to click button.')
      await bot.wait_for_interaction_to_be_over(bot, message_edit_response[1])
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Hit The Ball\" mini-game because of Discord button-clicking ratelimit.")
      success('Work || Finished waiting for interaction to be over.')
      return

    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Successfully completed the \"Hit The Ball\" mini-game.")

    success("Successfully completed the \"Hit The Ball\" mini-game.")
    return

  elif 'look at each color next to the words closely' in embed_content:
    word_to_color = {}
    for line in response.embeds[0].description.split('\n')[1:]:
      word_to_color[line.split('`')[1]] = line.split(':')[1]

    message_edit_response = await bot.safe_wait_for(bot, 'message_edit', check = lambda m, a: m.interaction is not None and m.interaction.user.id == bot.user.id and m.id == response.id)
    
    if message_edit_response is None:
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Look At Each Color Next To The Words Closely\" mini-game due to Dank Memer lag.")
      return error("Failed to wait for \"message edit\" event.")
    
    click_state = False
    wanted_word = message_edit_response[1].embeds[0].description.split('`')[1]
    for index, button in enumerate(message_edit_response[1].components[0].children):
      if button.label == word_to_color[wanted_word]:
        click_state = await bot.click(message_edit_response[1], 0, index)
        await asyncio.sleep(0.5)
        break
    
    if click_state is False:
      error('Work || Failed to click button.')
      await bot.wait_for_interaction_to_be_over(bot, message_edit_response[1])
      if bot.customization['work_logging'] is True:
        await log_hook(bot, "Auto Work — Failed to complete the \"Look At Each Color Next To The Words Closely\" mini-game because of Discord button-clicking ratelimit.")
      success('Work || Finished waiting for interaction to be over.')
      return

    if bot.customization['work_logging'] is True:
      await log_hook(bot, "Auto Work — Successfully completed the \"Look At Each Color Next To The Words Closely\" mini-game.")
    
    success("Successfully completed the \"Look At Each Color Next To The Words Closely\" mini-game.")
    return
  
  else:
    print(embed_content)

# Assisting functions

async def auto_powerup(bot, name, amount_ = None):
  import asyncio, datetime
  
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break
  
  if bot.powerups[name] is False:
    return True
  if name not in bot.last_used:
    bot.last_used[name] = 0
  cooldown = powerups_cooldown(name)
  if cooldown is None:
    return True
  if time.time() - bot.last_used[name] <= cooldown:
    return True

  amount = bot.powerups[f"{name}_amount"] if amount_ is None else int(amount_)
  quote = "\""
  readable_time = None

  if amount <= 0:
      darkend(f'The powerup {name} amount is now 0. Will be automatically bought from now on.')
      if bot.customization['autobuy_logging'] is True:
        await log_hook(bot, text = f"Auto Buy Powerups — Bot has ran out of the powerup `{name}`. {'Initiating auto-buy process.' if bot.customization['autobuypowerups'] is True else f'Please turn on {quote}Auto Buy{quote} in order for the bot to buy the powerup and re-use it.'}")
      state = await auto_buy_powerup(bot, name)
      if state is False:
        return True
      darkend(f'Successfully bought a `{name}`.')
      if bot.customization['autobuy_logging'] is True:
        await log_hook(bot, text = f"Auto Buy Powerups — Successfully bought a `{name}`.")
    
  readable_time = str(datetime.timedelta(seconds=powerups_cooldown(name)))

  status = await bot.use_powerup(bot, name)
  if status['status'] == 'unknown':
    if bot.customization['powerup_logging'] is True:
      await log_hook(bot, f'Auto Powerup — Faced an unknown issue while attempting to use the powerup `{name}`.')
    darkend(f'Faced an unknown issue while attempting to use the powerup `{name}`.')
    bot.last_used[name] = time.time()
    return
  if status['status'] == 'active':
    if bot.customization['powerup_logging'] is True:
      await log_hook(bot, f'Auto Powerup — The powerup `{name}` is already active.')
    darkend(f'The powerup `{name}` is already active.')
    bot.last_used[name] = time.time()
    return
  if status['status'] == 'blocked':
    darkend(f'The usage of the powerup `{name}` has been blocked because of an ongoing interaction.')
    bot.last_used[name] = time.time()
    return True
  if status['status'] == "doesn't own":
    darkend(f'Bot doesn\'t have a `{name}`.')
    if bot.customization['autobuy'] is False:
      darkend(f'Bot can\'t buy a `{name}` because "Auto Buy Powerups" is disabled.')
      if bot.customization['autobuy_logging'] is True:
        await log_hook(bot, text = f"Auto Buy Powerups — Cannot buy a `{name}` because \"Auto Buy Powerups\" is disabled.")
    return True


  # if status['status'] == 'used': Everything under is for this statement

  if amount_ is not None:
    amount_ -= 1

  bot.powerups[f"{name}_amount"] -= 1
  
  success(f'Used the powerup {name}. {bot.powerups[f"{name}_amount"]} remaining to be used. Will sleep for {Fore.WHITE}{powerups_cooldown(name)}{Fore.GREEN} seconds.')
  if (bot.powerups[f"{name}_amount"] <= 0
  and bot.customization['powerup_logging'] is True):
    await log_hook(bot, f'Auto Powerup — Used the powerup `{name}`. Time until reuse: `{readable_time}`')
  bot.last_used[name] = time.time()
  return

async def auto_buy_tool(bot, tool):
  import asyncio
  balance, bank = 0, 0
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break
  
  if bot.customization['autotool'] is False:
    darkend(f"Couldn't buy a `{tool}` because \"Auto Tool\" is disabled.")
    if bot.customization['autotool_logging']:
        await log_hook(bot, f"Auto Tool — Couldn't buy a `{tool}` because \"Auto Tool\" is disabled.")
    return False

  bot.internal['autobuying_busy'] = True
  bank_money_state = False

  darkend(f'Buying {tool}.')
  balance, bank = await bot.get_balance_and_bank(bot)
  darkend(f'Balance: {balance}\nBank: {bank}')
  
  quantity = await bot.get_item_quantity(bot, tool)
  darkend(f'Bot owns {quantity} {tool}.')

  if quantity != 0:
    darkend(f"Somehow the bot obtained {quantity} {tool}.")
    return True
  
  bank_money_state = bank > (25000 - balance)
  needed_money = 25000 - balance

  if int(balance) >= 25000:
    success(f'Balance is enough to buy a `{tool}`.')
    buy_state = await bot.buy_item(bot, tool)
    if buy_state is False:
      darkend(f'Failed to buy a `{tool}`.')
      if bot.customization['autotool_logging']:
        await log_hook(bot, f"Auto Tool — Failed to buy a `{tool}`.")
      return False

    success(f'Bought a `{tool}`.')
    if bot.customization['autotool_logging']:
      await log_hook(bot, f"Auto Tool — Bought a `{tool}`.")
    return True

  if bank_money_state is True:

    if bot.customization['withdraw'] is False:
      error(f'Balance is not enough to buy a `{tool}`. \"Auto Withdraw\" is required.')
      if bot.customization['autotool_logging']:
        await log_hook(bot, f"Auto Tool — Balance is not enough to buy a `{tool}`, please enable \"Auto Withdraw\" in order for the tool to be bought.")
      return False

    elif 0 > needed_money:
      error(f'Balance is not enough to buy a `{tool}`.')
      if bot.customization['autotool_logging']:
        await log_hook(bot, f"Auto Tool — Balance is not enough to buy a `{tool}`.")
      return False

    elif needed_money > bank:
      error(f'Bank is not enough to buy a `{tool}`.')
      if bot.customization['autotool_logging']:
        await log_hook(bot, f"Auto Tool — Balance & Bank is not enough to buy a `{tool}`.")
      return False

    else:

      print(f"{bot.user} || Bank: {bank} || Balance: {balance} || Needed money: {needed_money}")
      withdraw_state = await bot.withdraw(bot, needed_money)

      if withdraw_state is True:
        darkend(f"Withdrawn {needed_money}.")
        await bot.buy_tool(bot, tool)
        if bot.customization['autotool_logging']:
          await log_hook(bot, f"Auto Tool — Bought a `{tool}`.")
        return True
      else:
        darkend(f"Bot can't withdraw {needed_money}.")
        if bot.customization['autotool_logging']:
          await log_hook(bot, f"Auto Tool — Failed to withdraw & buy a `{tool}`.")
        return False

  if bank_money_state is False:
    darkend(f"{bot.user} || Balance & Bank are not enough to purchase `{tool}`.")
    if bot.customization['autotool_logging']:
      await log_hook(bot, f"Auto Tool — Balance & Bank are not enough to purchase `{tool}`.")
    return False

async def auto_buy_powerup(bot, item):
  import asyncio
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(0.5)
      continue
    break
    
  valid_name = powerups_valid_name(item)

  if bot.customization['autobuypowerups'] is False:
    darkend(f"Couldn't buy a `{valid_name}` because \"Auto Buy Powerups\" is disabled.")
    if bot.customization['autobuy_logging']:
      await log_hook(bot, f"Auto Buy Powerups — Couldn't buy a `{valid_name}` because \"Auto Buy Powerups\" is disabled.")
    return False

  balance, bank = 0, 0
  bot.internal['autobuying_busy'] = True
  check_price = powerup_to_price(item)
  cooldown = powerups_cooldown(item)
  channel = await bot.return_channel(bot)

  if check_price is False:
    error(f'Skipping the process of buying the item {valid_name} due to the item being unpurchasable.')
    if bot.customization['autobuy_logging']:
      await log_hook(bot, f"Auto Buy Powerups — Skipping the process of buying the item `{valid_name}` due to the item being unpurchasable.")
    return False

  darkend(f'Buying `{valid_name}`.')
  balance, bank = await bot.get_balance_and_bank(bot)

  bank_money_state = bank > (25000 - balance)
  needed_money = abs(25000 - balance)
  if balance >= check_price:
    success(f'Balance is enough to buy a `{valid_name}`.')
    buy_state = await bot.buy_item(bot, valid_name)
    if buy_state is False:
      success(f'Failed to buy a `{valid_name}`.')
      if bot.customization['autobuy_logging']:
        await log_hook(bot, f"Auto Buy Powerups — Failed to buy a powerup `{item}`.")    
      return False
    success(f'Bought `{valid_name}`.')
    # if bot.customization['autobuy_logging']:
    #   await log_hook(bot, f"Auto Buy Powerups — Bought the powerup `{item}`.")    
    # when its true the function that called it makes the log
    return True

  if bank_money_state is True:
    if bot.customization['withdraw'] is False:
      error(f'Balance is not enough to buy a `{valid_name}`.')
      if bot.customization['autobuy_logging']:
        await log_hook(bot, f"Auto Buy Powerups — Balance is not enough to buy a `{item}`. Please enable \"Auto Withdraw\" in order for the item to be bought.")
      return False

    withdraw_state = await bot.withdraw(bot, needed_money)
    if withdraw_state is True:
      darkend(f"Withdrawn {needed_money}.")
      buy_state = await bot.buy_item(bot, valid_name)
      if buy_state is False:
        success(f'Failed to buy a `{valid_name}`.')
        if bot.customization['autobuy_logging']:
          await log_hook(bot, f"Auto Buy Powerups — Failed to buy a powerup `{item}`.")    
        return False
      success(f'Bought `{valid_name}`.')
      # if bot.customization['autobuy_logging']:
      #   await log_hook(bot, f"Auto Buy Powerups — Bought the powerup `{item}`.")
      # when its true the function that called it makes the log
      return True
    else:
      darkend(f"Bot can't withdraw {needed_money}.")
      if bot.customization['autobuy_logging']:
        await log_hook(bot, f"Auto Buy Powerups — Balance & Bank are not enough to purchase `{valid_name}`. Skipping the process of buying the item.")
    return False

  if bank_money_state is False:
    if bot.customization['autobuy_logging']:
      await log_hook(bot, f"Auto Buy Powerups — Balance & Bank are not enough to purchase `{valid_name}`. Skipping the process of buying the item.")
    return False

async def fish_event(bot, message):
  newline = '\n'

  type_0 = "<:emptyspace:827651824739156030>"
  type_1 = "<:emptyspace:827651824739156030><:emptyspace:827651824739156030>"

  correct_button = 0
  if message.embeds[0].description.split(newline)[1].startswith(type_0):
    correct_button = 1
  if message.embeds[0].description.split(newline)[1].startswith(type_1):
    correct_button = 2
  click_state = await bot.click(message, 0, correct_button)

  if click_state is False:
    error(f'Fish || Failed to click button.')
    while True:
      message_edit_response = await bot.safe_wait_for(bot, 'message_edit', check = lambda m, a:
      m.interaction is not None
      and m.interaction.user.id == bot.user.id
      and m.id == message.id)
      try:
        if all([button.disabled for button in message_edit_response[1].components[0].children]) is True:
          break
      except:
        break
    success(f'Fish || Finished waiting for interaction to be over.')
    return True

  darkend(f"Sniped Fish event: {message.jump_url}")
  await log_hook(bot, f"Event Sniper — [Sniped Fish event]({message.jump_url}).")
  return True

async def hunt_event(bot, message):
  newline = '\n'

  # default is left side
  type_0 = "<:emptyspace:827651824739156030>" # in middle
  type_1 = "<:emptyspace:827651824739156030><:emptyspace:827651824739156030>" # right side

  correct_button = 1
  if message.embeds[0].description.split(newline)[2].startswith(type_0):
    correct_button = 2
  if message.embeds[0].description.split(newline)[2].startswith(type_1):
    correct_button = 1
  click_state = await bot.click(message, 0, correct_button)

  if click_state is False:
    error(f'Hunt || Failed to click button.')
    while True:
      message_edit_response = await bot.safe_wait_for(bot, 'message_edit', check = lambda m, a:
      m.interaction is not None
      and m.interaction.user.id == bot.user.id
      and m.id == message.id)
      try:
        if all([button.disabled for button in message_edit_response[1].components[0].children]) is True:
          break
      except:
        break
    success(f'Hunt || Finished waiting for interaction to be over.')
    return True

  darkend(f"Sniped Hunt event: {message.jump_url}")
  await log_hook(bot, f"Event Sniper — [Sniped Hunt event]({message.jump_url}).")
  return True

# Other

async def update_presence(bot):
  import asyncio
  while True:
    if bot.config['account_presence'] == str(bot.status):
      break
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      await asyncio.sleep(2.5)
      continue
    
    await bot.change_presence(status = custom_status(bot))
    bot.internal['waiting_presence'] = None
    return

async def presence_changer(bot):
  import asyncio
  while True:
    if (bot.messenger.internal[bot.user.id]['autofarming'] is False
    or bot.config['account_presence'] == str(bot.status)
    or bot.internal['waiting_presence'] == str(bot.status)):
      await asyncio.sleep(2.5)
      continue

    bot.loop.create_task(update_presence(bot))
    bot.internal['waiting_presence'] = str(bot.status)
    await asyncio.sleep(2.5)

async def log_hook(bot, text):
  from discord import Webhook
  import aiohttp, time

  text = f"**{bot.user}** || {text}"
  if len(bot.data['webhook_url']) == 0:
    return
  
  try:
    if bot.customization['embed_hooks'] is False:
      async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(bot.data['webhook_url'], session=session)
        if bot.customization['timestamps_logging'] is True:
          return await webhook.send(f"**<t:{round(time.time())}:t>:** {text}", username = 'Darkend', avatar_url = 'https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/logo.png')
        await webhook.send(text, username = 'Darkend', avatar_url = 'https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/logo.png')
    
    else:
      embed = discord.Embed(title = text.split(' — ')[0], description = f"**<t:{round(time.time())}:t>:** {text.split(' — ')[1]}", color = 0x00000)
      if bot.customization['timestamps_logging'] is True:
        embed.description = text.split(' — ')[1]
      embed.set_footer(text = 'Darkend || By Sxvxge', icon_url = 'https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/logo.png')
      
      async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(bot.data['webhook_url'], session=session)
        await webhook.send(embed=embed, username = 'Darkend', avatar_url = 'https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/logo.png')
  
  except Exception as e:
    error(f"{bot.user} | Webhook logging | {e}")

async def check_if_false(bot):
  import asyncio
  while True:
    if bot.messenger.internal[bot.user.id]['autofarming'] is False:
      bot.messenger.internal[bot.user.id]['autofarming'] = None
      exit()
    else:
      await asyncio.sleep(5)

async def cache_powerups_task(bot):
  import asyncio, datetime
  while True:
    channel = await bot.return_channel(bot)

    darkend("Caching powerups...")
    state = await bot.cache_powerups(bot)

    active_items = bot.internal['active_items']

    check_time_to_sleep = int(active_items[min(active_items, key = active_items.get)]) if state is True else 2100
    sleep_time = 2100 if check_time_to_sleep > 2100 else check_time_to_sleep

    readable_time = str(datetime.timedelta(seconds=sleep_time))
    darkend(f"Sleeping for: {readable_time}")
    await asyncio.sleep(sleep_time)
    continue

async def start_scraping_inventory(bot):
  import asyncio
  from utils.useful import update_html
  while True:
    if bot.messenger.internal[bot.user.id]["start_scraping"] is False:
      await asyncio.sleep(0.5)
      continue
    # success("Initiating scrape command...")
    items, pages = [], 0
    all_items = {'all_items': []}
    safe_to_go = True
    message_id = None
    inventory_message_id = 0

    while True:
      channel = await bot.return_channel(bot)
      message = await bot.force_send(bot, command = 'inventory')
      response = await bot.safe_wait_for(bot, 'message', check = lambda m:  m.author.id == 270904126974590976 and m.channel.id == channel.id and m.interaction.user.id == bot.user.id, timeout = 5)
      if response is None:
        error(f"Error while trying to scrape inventory || Step 1")
        await asyncio.sleep(0.5)
        continue
      else:

        if 'Yikes' in response.embeds[0].description:
          safe_to_go = False
          break
        
        if 'You have an ongoing command running.' in response.embeds[0].description:
          await asyncio.sleep(30)

        elif (bot.user.name in response.embeds[0].author.name):
          pages = int(response.embeds[0].footer.text.split('of ')[1])
          bot.messenger.internal[bot.user.id]['scraper_max_pages'] = pages
          message_id = response.id
          break

        misc("Inventory Scraper || Step 2 || Both checks failed. Continuing...")
        continue
    
    if safe_to_go is False:
      error("User apparently has no items in the inventory. Will use the empty inventory text.")
      bot.messenger.internal[bot.user.id]["scraper_pages"] = [empty_inventory_text]
      bot.messenger.internal[bot.user.id]["scraper_working"] = False
      bot.messenger.internal[bot.user.id]["start_scraping"] = False
      return
  
    for i in range(pages + 1):
      for line in response.embeds[0].description.split('\n'):
        line = line.replace('`', '').replace('*', '')
        if line.startswith('<:') or line.startswith('<a:'):
          name = line.split('> ')[1].split(' ─')[0]
          amount = line.split('─ ')[1]
          if f'{amount} {name}' not in items:
            items.append(f'{amount} {name}')
            all_items["all_items"].append((amount, name))
      
      await bot.click(response, 1, 2)

      if i == pages + 1:
        for line in response.embeds[0].description.split('\n'):
          line = line.replace('`', '').replace('*', '')
          if line.startswith('<:') or line.startswith('<a:'):
            name = line.split('> ')[1].split(' ─')[0]
            amount = line.split('─ ')[1]
            if f'{amount} {name}' not in items:
              items.append(f'{amount} {name}')
              all_items["all_items"].append((amount, name))

      await asyncio.sleep(1.25)

    _message_ = await channel.fetch_message(message_id)

    for line in _message_.embeds[0].description.split('\n'):
      line = line.replace('`', '').replace('*', '')
      if line.startswith('<:') or line.startswith('<a:'):
        bot.messenger.internal[bot.user.id]["scraper_last_page_item_amount"] += 1
    
    rich_text_pages_list = update_html(bot, all_items)
    data = await bot.get_bot_data(bot)

    bot.messenger.internal[bot.user.id]["scraper_pages"] = rich_text_pages_list
    bot.messenger.internal[bot.user.id]["scraper_working"] = False
    bot.messenger.internal[bot.user.id]["start_scraping"] = False
    bot.messenger.internal[bot.user.id]["profile_data"] = data
    
async def auto_typing(bot):
  import asyncio
  while True:
    settings = get_account_settings(bot.internal['account_id'])
    if (settings['config']['aTyping'] is False
    or bot.messenger.internal[bot.user.id]['autofarming'] is False):
      await asyncio.sleep(2.5)
      continue
    
    channel = await bot.return_channel(bot)
    try:
      await channel.trigger_typing()
    except:
      continue

    await bot.safe_wait_for(bot, 'message', check = lambda m: m.author.id == bot.user.id and m.channel.id == channel.id, timeout = 10)

    continue
  
async def update_data(bot):
  import asyncio
  try:
    while True:
      settings = get_account_settings(bot.internal['account_id'], create = False)
      if settings is None:
        error(f"{bot.user} || Data is none.")
        return
      bot.settings = settings
      bot.data = settings["data"]
      bot.config = settings["config"]
      bot.powerups = settings["powerups"]
      bot.customization = settings["customization"]

      await asyncio.sleep(2.5)
  except:
    pass

async def get_item_prices(bot):
  import asyncio
  all_items = [
    "aplus", "ant",
    "banhammer", "beaker",
    "bean", "boar",
    "fish", "cookie",
    "corncob", "corndog",
    "deer", "dragon",
    "duck", "ectoplasm",
    "energydrink", "exoticfish",
    "fossil", "bread",
    "garbage", "jellyfish",
    "junk", "kraken",
    "ladybug", "lawdegree",
    "legendaryfish",
    "tree", "memepills", "meteorite",
    "note", "potato",
    "rabbit", "rarefish",
    "seaweed", "skunk",
    "spider", "starfragment",
    "stickbug",
    "trash", "vaccine", "worm"
  ]
  item_prices = {}
  for item in all_items:
    channel = await bot.return_channel(bot)
    message = await bot.send(bot, command = 'shop', item = item)
    response = await bot.safe_wait_for(bot, 'message', check = lambda m: m.author.id == 270904126974590976 and m.channel.id == channel.id  and item in m.embeds[0].fields[2].value.lower(), timeout = 5)
    if response is None:
      await asyncio.sleep(3.5)
      continue
  
    description = response.embeds[0].description.lower().replace('*', '')
    trade_price = description.split('trade - ⏣ ')[1].replace(',', '').split(' ')[0]
    item_prices[item] = int(trade_price)
    await asyncio.sleep(0.5)
    print(item_prices)
  print(f"Final: {item_prices}")

async def command_executor(bot):
  import asyncio, random

  highlow_cooldown = commands_cooldown(bot, 'highlow')
  trivia_cooldown  = commands_cooldown(bot, 'trivia')
  scratch_cooldown = commands_cooldown(bot, 'scratch')
  deposit_cooldown = commands_cooldown(bot, 'deposit')

  gambling_commands = ['slots', 'gamble', 'snakeeyes']
  button_commands = [['search', 'auto_search', 2], ['crime', 'auto_crime', 2], ['postmemes', 'auto_meme', 4]]
  raw_commands = [['fish', 'auto_fish'], ['hunt', 'auto_hunt'],  ['beg', 'auto_beg'], ['dig', 'auto_dig']]
  powerup_commands = ['pizza', 'horseshoe', 'ammo', 'alcohol', 'apple', 'taco', 'fishingbait', 'whiskey', 'prestige', 'robbersmask']

  while True:
    if bot.messenger.internal[bot.user.id]["crash"] is True:
      return

    # Powerups
    for item in powerup_commands:
      try:
        if bot.powerups[item] is True:
          state = await auto_powerup(bot, item)
          if bot.config['command_delay'] is True:
            await asyncio.sleep(random.randrange(6, 8))
          # success("Moving to the next command :D")
      except Exception as e:
        error(f"Error in the command 'Use {item}': {e}")

    # Separate
    try:
      if bot.config['work'] is True:
        state = await auto_work(bot)
        if bot.config['command_delay'] is True:
          await asyncio.sleep(random.randrange(2, 4))
    except Exception as e:
      error(f"Error in the command 'Work': {e}")
    try:
      if bot.config['auto_highlow'] is True:
        state = await auto_highlow(bot, highlow_cooldown)
        if bot.config['command_delay'] is True:
          await asyncio.sleep(random.randrange(2, 4))
    except Exception as e:
      error(f"Error in the command 'HighLow': {e}")

    try:
      if bot.config['auto_trivia'] is True:
        state = await auto_trivia(bot, trivia_cooldown)
        if bot.config['command_delay'] is True:
          await asyncio.sleep(random.randrange(2, 4))
    except Exception as e:
      error(f"Error in the command 'Trivia': {e}")

    try:
      if bot.config['scratch'] is True:
        state = await auto_scratch(bot, scratch_cooldown)
        if bot.config['command_delay'] is True:
          await asyncio.sleep(random.randrange(2, 4))
    except Exception as e:
      error(f"Error in the command 'Scratch': {e}")

    # Gamble
    for gamble_command in gambling_commands:
      try:
        if bot.config[gamble_command] is True:
          state = await gamble_tasks(bot, gamble_command, gamble_command)
          if bot.config['command_delay'] is True:
            await asyncio.sleep(random.randrange(2, 4))
      except Exception as e:
        error(f"Error in the command '{gamble_command}': {e}")
    
    # Button
    for button_command in button_commands:
      try:
        if bot.config[button_command[1]] is True:
          state = await button_tasks(bot, button_command[0], button_command[1], button_command[2])
          if bot.config['command_delay'] is True:
            await asyncio.sleep(random.randrange(2, 4))
      except Exception as e:
        error(f"Error in the command '{button_command[0]}': {e}")
      
    # Raw
    for raw_command in raw_commands:
      try:
        if bot.config[raw_command[1]] is True:
          state = await raw_tasks(bot, raw_command[0], raw_command[1])
          await asyncio.sleep(random.randrange(2, 4))
      except Exception as e:
        error(f"Error in the command '{raw_command[0]}': {e}")

    # Seaparate (2)
    try:
      if bot.config['auto_dep']:
        state = await auto_deposit(bot, deposit_cooldown)
        await asyncio.sleep(random.randrange(2, 4))
    except Exception as e:
      error(f"Error in the command 'Deposit': {e}")
  
    await asyncio.sleep(2.5)

async def crash(bot : discord.Client):
  import asyncio
  try:
    while True:
      if bot.messenger.internal[bot.user.id]["crash"] is False:
        await asyncio.sleep(2.5)
        continue
      break

    darkend(f"{bot.user} || Stopping the autofarm completely")
    await bot.close()
    bot.clear()
    for task in asyncio.Task.all_tasks():
      task.cancel()
    exit()
  except Exception as e:
    error(f"Crash error: {e}")

async def error_log(bot : discord.Client, error_data):
  import aiohttp, discord, datetime, psutil, platform, mystbin, random
  from discord import Webhook
  mystbin_client = mystbin.Client()
  all_settings = [
    'auto_beg', 'auto_dep', 'auto_fish', 
    'auto_highlow', 'auto_dig', 'auto_hunt', 
    'auto_search', 'auto_meme', 'auto_trivia', 
    'auto_crime', 'slots',
    'scratch', 'gamble', 'snakeeyes',
    'command_delay', 'premium_status'
  ]
  enabled_settings = ', '.join(item for item in all_settings if bot.config[item] is True)
  settings_paste = await mystbin_client.create_paste(
    filename = f"{bot.user.id}_settings_{random.randrange(100, 1500)}",
    content = enabled_settings,
    syntax="txt",
  )
  traceback_paste = await mystbin_client.create_paste(
    filename = f"{bot.user.id}_traceback_{random.randrange(100, 1500)}",
    content = error_data['traceback'],
    syntax="py",
  )
  appropriate_traceback = error_data['traceback'] if len(error_data['traceback']) < 1000 else traceback_paste
  system_information = f""" ```yaml
PC Name: {platform.node()}
Windows Version: Windows {platform.release()}
Dish Space: {str(psutil.disk_usage('/')[0] / 1024 ** 3).split(".")[0]}GB
Ram: {str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]}GB
```
  """
  bot_information = f"""```yaml
Settings: {settings_paste}
Autofarm Time: {str(datetime.timedelta(seconds = round(float(time.time() - bot.internal['started_at']))))}
```
  """
  error_information = f"""```py
# Event: {error_data['event']}

{appropriate_traceback}
```
  """
  embed = discord.Embed(
    title = f"Darkend — Error",
    color = 0x00000
  )
  embed.add_field(
    name = "System Information",
    value = system_information,
    inline = True
  )
  embed.add_field(
    name = "Bot Data",
    value = bot_information,
    inline = True
  )
  embed.add_field(
    name = "Error",
    value = error_information,
    inline = False
  )
  embed.set_footer(
  text = 'Darkend || By Sxvxge',
  icon_url = 'https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/logo.png'
  )
  async with aiohttp.ClientSession() as session:
    webhook = Webhook.from_url(bot.internal['error_hook'], session=session)
    await webhook.send(embed=embed, username = 'Darkend', avatar_url = 'https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/logo.png')
  await mystbin_client.close()
  error(f"Error logged: {traceback_paste}")

async def item_prices(bot, response):
  import asyncio, json

  pages = int(response.embeds[0].footer.text.split('of ')[1])
  channel = await bot.return_channel(bot)
  current_page = 0
  items = {}

  for i in range(pages):
    lines_to_check = [line.replace('*', '') for line in response.embeds[0].description.split('\n') if '─' in line]
    for line in lines_to_check:
      name = line.split('> ')[1].split(' ─')[0]
      amount = int(''.join(x for x in line.split('─')[1] if x.isnumeric()))
      items[name] = amount

    if current_page != 6:
      await asyncio.sleep(1.5)
      state = await bot.click(response, 1, 2)
      response = await bot.safe_wait_for(bot, 'message_edit', check = lambda b, a: a.interaction is not None and a.interaction.user.id == bot.user.id and a.channel.id == channel.id)
      response = response[1]
      current_page = int(response.embeds[0].footer.text.split('Page ')[1].split(' of')[0])

  await channel.send(f"```json\n{json.dumps(items, indent = 4, sort_keys = True)}```")