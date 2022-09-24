from email.policy import default
import json, os, ast

from utils.useful import error, success, darkend, misc

appdata = os.getenv('APPDATA')
directory = f"{appdata}\\Darkend v1"
alt_handler_directory = f"{directory}\\Darkend Alt Handler"

def create_account_file(account_id):
  path = f"{alt_handler_directory}\\{account_id}.json"
  if account_id is None:
    return error("Cannot make a file for an account ID being None.")
  if os.path.isfile(path):
    return
  
  error(f"There is no existing settings file for the account with the ID {account_id}.")
  with open(path, "w+") as file:
    file.write(default_settings())
  return success(f"A settings file for the account with the ID {account_id} has been made.")

def update_account_settings(account_id, data):
  # Confirm there was a settings file first
  create_account_file(account_id)

  path = f"{alt_handler_directory}\\{account_id}.json"
  with open(path, "w+") as file:
    file.write(json.dumps(data, indent = 2, sort_keys = False))

def get_account_settings(account_id, /, create = True):
  # Confirm there was a settings file first
  if create is True:
    create_account_file(account_id)
  
  try:
    path = f"{alt_handler_directory}\\{account_id}.json"
    with open(path, "r") as file:
      data = file.read()
    
    return json.loads(data)
  except:
    return None

def get_all_accounts_data():
  data = {}
  
  if len(os.listdir(alt_handler_directory)) == 0:
    return None

  for file in os.listdir(alt_handler_directory):
    data_recieved = get_account_settings(file.split('.')[0])
    
    token = data_recieved["data"]["token"]
    channel_id = data_recieved["data"]["channel_id"]
    webhook_url = data_recieved["data"]["webhook_url"]
    account_id = data_recieved["data"]["account_id"]

    data[token] = {"channel_id": channel_id, "webhook_url": webhook_url, "account_id": account_id}
  
  return data

def ensure_new_keys_get_added(account_id):
  default_data = json.loads(default_settings())
  user_data = get_account_settings(account_id)

  for key, value in default_data.items():
    if key not in user_data.keys():
      user_data[key] = value
  
    for nested_key in default_data[key]:
      if nested_key not in user_data[key]:
        user_data[key][nested_key] = default_data[key][nested_key]
  
  update_account_settings(account_id, user_data)
  user_data = get_account_settings(account_id)

  for key, value in default_data.items():

    for nested_key in list(user_data[key]):
      if nested_key not in default_data[key]:
        del user_data[key][nested_key]

  update_account_settings(account_id, user_data)

def view_account_logs(account_id):
  create_account_file(account_id)

  path = f"{alt_handler_directory}\\{account_id}_logs.darkend"
  if os.path.isfile(path) is False:
    with open(path, "w+") as file:
      file.write("")
  os.system(f"notepad {path}")
  exit()

def default_settings():
  settings = """{
 "data": {
    "token": "",
    "account_id": 0,
    "channel_id": 0,
    "webhook_url": ""
 },
 "config" : {
    "auto_beg": false,
    "auto_dep": false,
    "auto_fish": false,
    "auto_highlow": false,
    "auto_dig": false,
    "auto_hunt": false,
    "auto_search": false,
    "auto_meme": false,
    "auto_trivia": false,
    "auto_crime": false,
    "search_places": [],
    "crime_actions": [],
    "resume_after_scraping": false,
    "scraper_alert": false,
    "scraper_retry": false,
    "account_presence": "online",
    "premium_status": false,
    "slots": false,
    "slots_bet": 1,
    "scratch": false,
    "scratch_bet": 1500,
    "gamble": false,
    "gamble_bet": 1500,
    "snakeeyes": false,
    "snakeeyes_bet": 1500,
    "command_delay": false,
    "work": false,
    "preferred_job": "Automatic",
    "dm_mode": false
 },
 "powerups" : {
    "pizza": false,
    "pizza_amount": 0,
    "horseshoe": false,
    "horseshoe_amount": 0,
    "ammo": false,
    "ammo_amount": 0,
    "alcohol": false,
    "alcohol_amount": 0,
    "apple": false,
    "apple_amount": 0,
    "taco": false,
    "taco_amount": 0,
    "fishingbait": false,
    "fishingbait_amount": 0,
    "prestige_amount" : 0,
    "prestige" : false,
    "robbersmask_amount" : 0,
    "robbersmask" : false,
    "whiskey_amount" : 0,
    "whiskey" : false,
    "boots": false,
    "boots_amount": false
 },
 "customization" : {
    "autofarm_logging" : false,
    "powerup_logging" : false,
    "autobuy_logging" : false,
    "levelup_logging" : false,
    "death_logging" : false,
    "timestamps_logging" : false,
    "deathlifesaver" : false,
    "embed_hooks" : false,
    "withdraw" : false,
    "autotool": false,
    "autotool_logging": false,
    "autobuypowerups": false,
    "work_logging": false,
    "event_sniping": false,
    "event_sniping_mode": "whitelist",
    "event_sniping_servers": [],
    "event_sniping_logging": false
 }
}"""

  return settings