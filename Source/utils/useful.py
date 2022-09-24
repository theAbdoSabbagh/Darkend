import os, requests
from colorama import init, Fore
init(autoreset = True)

fonts_count = 0

# Paths
appdata = os.getenv('APPDATA')
directory = f"{appdata}\\Darkend v1"
alt_handler_directory = f"{appdata}\\Darkend v1\\Darkend Alt Handler"
gothic_century = f'{directory}\\Century Gothic.ttf'
gothic_century_bold = f'{directory}\\GOTHICB.TTF'
cascadia_mono = f'{directory}\\Cascadia Mono.ttf'
cascadia_bold = f'{directory}\\CascadiaMono-Bold.ttf'

def get_domain(query):
  return f'http://darkend.tech/{query}'

def download_resources(url, name, /, check_first = True):
  if check_first is True:
    if os.path.isfile(f"{directory}\\{name}"):
      return

  response = requests.get(url)
  with open(f"{directory}\\{name}", 'wb') as file:
    file.write(response.content)

def infinite_check():
  while True:
    darkend_folder()
    download_resources(get_domain('res/Century Gothic.ttf'), 'Century Gothic.ttf')
    download_resources(get_domain('res/GOTHICB.TTF'), 'GOTHICB.TTF')
    download_resources(get_domain('res/CascadiaMono-Regular.ttf'), 'Cascadia Mono.ttf')
    download_resources(get_domain('res/CascadiaMono-Bold.ttf'), 'CascadiaMono-Bold.ttf')
    download_resources("https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/trivia.json", 'trivia.json')

def install_font():
  global fonts_count
  fonts = {
    gothic_century : 'Century Gothic.ttf',
    gothic_century_bold : 'GOTHICB.TTF',
    cascadia_mono: 'Cascadia Mono.ttf',
    cascadia_bold: 'CascadiaMono-Bold.ttf'
  }
  for path, name in fonts.items():
    if name in os.listdir(r'C:\Windows\fonts'):
      fonts_count += 1
    else:
      error(f"{name} Font not installed.")
      import shutil, ctypes
      from ctypes import wintypes
      import winreg

      user32 = ctypes.WinDLL('user32', use_last_error=True)
      gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

      FONTS_REG_PATH = 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts'

      HWND_BROADCAST   = 0xFFFF
      SMTO_ABORTIFHUNG = 0x0002
      WM_FONTCHANGE    = 0x001D
      GFRI_DESCRIPTION = 1
      GFRI_ISTRUETYPE  = 3

      if not hasattr(wintypes, 'LPDWORD'):
          wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

      user32.SendMessageTimeoutW.restype = wintypes.LPVOID
      user32.SendMessageTimeoutW.argtypes = (
          wintypes.HWND,   # hWnd
          wintypes.UINT,   # Msg
          wintypes.LPVOID, # wParam
          wintypes.LPVOID, # lParam
          wintypes.UINT,   # fuFlags
          wintypes.UINT,   # uTimeout
          wintypes.LPVOID) # lpdwResult

      gdi32.AddFontResourceW.argtypes = (
          wintypes.LPCWSTR,) # lpszFilename

      gdi32.GetFontResourceInfoW.argtypes = (
          wintypes.LPCWSTR, # lpszFilename
          wintypes.LPDWORD, # cbBuffer
          wintypes.LPVOID,  # lpBuffer
          wintypes.DWORD)   # dwQueryType
      # copy the font to the Windows Fonts folder
      dst_path = os.path.join(os.environ['SystemRoot'], 'Fonts',
                              os.path.basename(path))
      shutil.copy(path, dst_path)
      # load the font in the current session
      for i in range(100):
        try:
          if not gdi32.AddFontResourceW(dst_path):
            os.remove(dst_path)
        except:
          continue
        else:
          break

      # notify running programs
      user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0,
                                 SMTO_ABORTIFHUNG, 1000, None)
      # store the fontname/filename in the registry
      filename = os.path.basename(dst_path)
      fontname = os.path.splitext(filename)[0]
      # try to get the font's real name
      cb = wintypes.DWORD()
      if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), None,
                                    GFRI_DESCRIPTION):
          buf = (ctypes.c_wchar * cb.value)()
          if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), buf,
                                        GFRI_DESCRIPTION):
              fontname = buf.value
      is_truetype = wintypes.BOOL()
      cb.value = ctypes.sizeof(is_truetype)
      gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb),
          ctypes.byref(is_truetype), GFRI_ISTRUETYPE)
      if is_truetype:
          fontname += ' (TrueType)'
      with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, FONTS_REG_PATH, 0,
                          winreg.KEY_SET_VALUE) as key:
          winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)
      success("Font installed")
      fonts_count += 1

def error(text):
  text = str(text).replace('\n', '\n[Error] ')
  print(f"{Fore.RED}[Error] {text}")

def success(text):
  text = str(text).replace('\n', '\n[Success] ')
  print(f"{Fore.GREEN}[Success] {text}")

def darkend(text):
  text = str(text).replace('\n', '\n[Darkend] ')
  print(f"{Fore.CYAN}[Darkend] {text}")

def misc(text):
  text = str(text).replace('\n', '\n[Misc] ')
  print(f"{Fore.MAGENTA}[Misc] {text}")

def darkend_folder():
  if not os.path.exists(directory):
    os.makedirs(directory)
    success('Made directory')

def darkend_alt_handler_folder():
  if not os.path.exists(alt_handler_directory):
    os.makedirs(alt_handler_directory)
    success('Made alt handler directory')

async def log_trivia(question, answer):
  import json
  path = f"{directory}//trivia.json"
  
  with open(path, "r+") as trivia_file:
    data = json.loads(trivia_file.read())

  data[question] = answer

  with open(path, "w+") as trivia_file:
    trivia_file.write(json.dumps(data, indent = 2, sort_keys = False))

def custom_status(bot):
  import discord
  statuses = {
    'online' : discord.Status.online,
    'dnd' : discord.Status.dnd,
    'idle' : discord.Status.idle,
    'invisible' : discord.Status.invisible
  }

  return statuses[bot.config['account_presence']]

def useless():
  pass

def update_html(bot, data):
  import itertools
  base = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
  <head></head>
  <body style=" font-family:'Century Gothic'; font-size:13px; font-weight:400; font-style:normal;">
"""
  template = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
  <head></head>
  <body style=" font-family:'Century Gothic'; font-size:13px; font-weight:400; font-style:normal;">
"""
  pages = []
  if len(data["all_items"]) >= 8:
    for counter, list_ in zip(itertools.cycle(range(8)), data['all_items']):
      base += f'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">• {list_[0]}x {list_[1]}</p>'
      if counter == 7:
        pages.append(f"""{base}
  </body>
</html>""")
        base = template

    base = template
    for list__ in data["all_items"][len(data["all_items"])-bot.messenger.internal[bot.user.id]['scraper_last_page_item_amount']:9999]:
      base += f'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">• {list__[0]}x {list__[1]}</p>'
    pages.append(f"""{base}
  </body>
</html>""")
    base = template

  else:
    for list___ in data["all_items"]:
      base += f'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">• {list___[0]}x {list___[1]}</p>'
    
    pages.append(f"""{base}
  </body>
</html>""")
    base = template
  return pages

def scraper_html_text(bot):
  min_ = bot.messenger.internal[bot.user.id]['scraper_current_page']
  if int(min_) < 0:
    min_ = 0
  return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /></head><body style=" font-family:'Century Gothic'; font-size:13px; font-weight:400; font-style:normal;">
<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Currently Viewing: Page {min_+1}/{bot.messenger.internal[bot.user.id]['scraper_max_pages']}</span></p></body></html>"""

def alt_scraper_html_text(min_, max_):
  if int(min_) < 0:
    print(f'Min is {min_}')
    min_ = 0
  return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /></head><body style=" font-family:'Century Gothic'; font-size:13px; font-weight:400; font-style:normal;">
<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Currently Viewing: Page {min_+1}/{max_}</span></p></body></html>"""

def unique_items_html(value):
  return f"<body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Unique Items: {value}</span></p></body></html>"

def bot_balance_html(value):
  return f"<body style=\" font-family:\'Century Gothic\'; font-size:15px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bot Balance: {value}</span></p></body></html>"

def bot_bank_html(value):
  return f"<body style=\" font-family:\'Century Gothic\'; font-size:15px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bot Bank: {value}</span></p></body></html>"

def networth_html(value):
  return f"<body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Bot Networth: {value}</span></p></body></html>"

def bot_level_html(value):
  return f"<body style=\" font-family:\'Century Gothic\'; font-size:15px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bot Level: {value}</span></p></body></html>"

def total_items_html(value):
  return f"<body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Total Items: {value}</span></p></body></html>"

def total_commands_html(value):
  return f"<body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Total Commands: {value}</span></p></body></html>"

def timer_to_seconds(string):
  import re
  matches = re.findall(r"(\d+)(\w)", string)
  to_multiply = {
    'd' : 86400,
    'h' : 3600,
    'm' : 60,
    's' : 1,
  }
  return sum(to_multiply[match[1]] * int(match[0]) for match in matches)