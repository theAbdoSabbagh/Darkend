from PyQt5 import QtCore, QtGui, QtWidgets
from alts_handler import shadow

close_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAUlJREFUaEPtmNEOgyAMRemXbn7Z3JeykGjCQ8W29yIhw9fNck4vq0xJk18yOX9aAqMTXAmsBMAOrC0ENhC+/f8SyDm/RWSHW6cUiNR2JZBzLuCvlNIuIhtTIlrbLFC6k1L6VNA0iQr+LL9ZUzYLlMrKQrCEUvMrIqVZpsslwJZA4QuPW4AlwYAPC6ASLHhIICrBhIcFvBJseIqAVaIHPE3gTqIXPFXgSuKYdOXpfV6uOX/3MAiN0VZRpdv116nw9ARO0gsJOvzTAvCxQ0v+6S1El6AKaNPm6Fr9I6ZK0ARao7LHKfbcThQBy5zvJQELWOAb0wneTpCAB76XRFggAt9DIiSAwLMl3AIMeKaES4AJz5IwCyivVWhnmxGvVWjwShKu2uYEqoXmfbV49+dixOfuBEZAttZcAqMTWQmsBMAOrC0ENhC+ffoEfn4d+DFO/D3mAAAAAElFTkSuQmCC'

def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

class Ui_WelcomeWindow(object):
    def setupUi(self, WelcomeWindow):
        WelcomeWindow.setObjectName("WelcomeWindow")
        WelcomeWindow.resize(700, 300)
        self.centralwidget = QtWidgets.QWidget(WelcomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.welcome_frame = QtWidgets.QFrame(self.centralwidget)
        self.welcome_frame.setGeometry(QtCore.QRect(0, 0, 10000, 10000))
        self.welcome_frame.setStyleSheet("background-color: rgba(17,24,39,255);")
        self.welcome_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.welcome_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.welcome_frame.setObjectName("welcome_frame")
        self.welcome_title = QtWidgets.QLabel(self.welcome_frame)
        self.welcome_title.setGeometry(QtCore.QRect(0, 80, 700, 50))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPixelSize(48)
        self.welcome_title.setFont(font)
        self.welcome_title.setStyleSheet("color: white;")
        self.welcome_title.setObjectName("welcome_title")
        self.website_button = QtWidgets.QPushButton(self.welcome_frame)
        self.website_button.setGeometry(QtCore.QRect(180, 150, 161, 41))
        self.website_button.setMaximumSize(QtCore.QSize(10000, 10000))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPixelSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.website_button.setFont(font)
        self.website_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.website_button.setStyleSheet("QPushButton {\n    background-color: transparent;\n    color: rgb(255, 255, 255);\n    border: 2px solid rgb(39,65,100);\n    border-radius: 5px;\n    text-align: center;\n\n}\nQPushButton::hover{\n    background-color: rgb(39,65,100);\n}\n")
        self.website_button.setIconSize(QtCore.QSize(30, 1000))
        self.website_button.setObjectName("website_button")
        self.multiple_accounts_button = QtWidgets.QPushButton(self.welcome_frame)
        self.multiple_accounts_button.setGeometry(QtCore.QRect(360, 150, 161, 41))
        self.multiple_accounts_button.setMaximumSize(QtCore.QSize(10000, 10000))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPixelSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.multiple_accounts_button.setFont(font)
        self.multiple_accounts_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.multiple_accounts_button.setStyleSheet("QPushButton {\n    background-color: rgb(39,65,100);\n    color: rgb(255, 255, 255);\n    border-radius: 5px;\n    text-align: center;\n\n}\nQPushButton::hover{\n    background-color: rgb(60, 94, 150);\n}\n")
        self.multiple_accounts_button.setIconSize(QtCore.QSize(30, 1000))
        self.multiple_accounts_button.setObjectName("multiple_accounts_button")
        self.close = QtWidgets.QPushButton(self.welcome_frame)
        self.close.setGeometry(QtCore.QRect(640, 10, 51, 41))
        self.close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close.setStyleSheet("QPushButton {\n    border: none;\n    background-color: transparent;\n}\nQPushButton::hover {\n    border-radius: 5px;\n    background-color: rgb(136, 8, 8);\n}")
        self.close.setText("")
        self.close.setIcon(iconFromBase64(close_icon_b64))
        self.close.setIconSize(QtCore.QSize(32, 32))
        self.close.setObjectName("close")

        WelcomeWindow.setCentralWidget(self.centralwidget)

        # Effects
        buttons_list = [
          self.website_button,
          self.multiple_accounts_button
        ]
        for item in buttons_list:
          effect = QtWidgets.QGraphicsDropShadowEffect(item)
          effect.setOffset(0, 0)
          effect.setColor(QtGui.QColor(39, 65, 100))
          effect.setBlurRadius(30)
          item.setGraphicsEffect(effect)

        self.website_button.clicked.connect(lambda: self.open_website())
        self.multiple_accounts_button.clicked.connect(lambda: self.open_multiple_accounts_window())
        self.close.clicked.connect(lambda: exit())

        self.retranslateUi(WelcomeWindow)
        QtCore.QMetaObject.connectSlotsByName(WelcomeWindow)

    def retranslateUi(self, WelcomeWindow):
        _translate = QtCore.QCoreApplication.translate
        WelcomeWindow.setWindowTitle(_translate("WelcomeWindow", "Darkend"))
        self.welcome_title.setText(_translate("WelcomeWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Darkend</span></p></body></html>"))
        self.website_button.setText(_translate("WelcomeWindow", "Website"))
        self.multiple_accounts_button.setText(_translate("WelcomeWindow", "Dashboard"))

    def open_website(self):
      import webbrowser
      webbrowser.open('https://darkend.tech')

    def open_multiple_accounts_window(self):
      from alts_handler import Ui_MultipleAccounts
      self.MultipleAccountWindow = QtWidgets.QMainWindow()
      self.ui = Ui_MultipleAccounts()
      self.ui.setupUi(self.MultipleAccountWindow)
      self.icon = QtGui.QIcon(iconFromBase64(logo_b64))
      self.MultipleAccountWindow.setWindowIcon(self.icon)
      self.MultipleAccountWindow.setFixedSize(838, 451)
      self.MultipleAccountWindow.setFont(font)
      MainWindow.hide()
      self.MultipleAccountWindow.show()
      if imported:
        pyi_splash.close()

def make_dpi_aware():
  import ctypes, platform
  if float(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

imported = False
try:
  import pyi_splash
except ImportError:
  pass
else:
  imported = True

def close_now():
  shadow.internal["config"]['close_now'] = True
  sys.exit()

async def version_check():
  import aiohttp
  
  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Versions/public_version') as r:
      public_version = await r.text()
    async with cs.get('https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Versions/private_version') as r:
      private_version = await r.text()

  version_state = False
  
  if (shadow.internal["versions"]["isPrivate"] is True
  and private_version.strip().replace('\n', '') == shadow.internal["versions"]["private_version"]):
    print(private_version.strip().replace('\n', ''), shadow.internal["versions"]["private_version"])
    version_state = True

  if (shadow.internal["versions"]["isPublic"] is True
  and public_version.strip().replace('\n', '') == shadow.internal["versions"]["public_version"]):
    print(public_version.strip().replace('\n', ''), shadow.internal["versions"]["public_version"])
    version_state = True
  
  return True, "http://darkend.tech", version_state

def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

if __name__ == "__main__":
  from utils.useful import (darkend_folder, install_font, download_resources,
                            darkend_alt_handler_folder, infinite_check, get_domain)
  import sys, asyncio
  from qasync import QEventLoop
  from threading import Thread
 
  logo_b64 = b'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'
  
  try:
    darkend_folder()
    darkend_alt_handler_folder()
    install_font()
    download_resources(get_domain('res/Century Gothic.ttf'), 'Century Gothic.ttf')
    download_resources(get_domain('res/GOTHICB.TTF'), 'GOTHICB.TTF')
    download_resources(get_domain('res/CascadiaMono-Regular.ttf'), 'Cascadia Mono.ttf')
    download_resources(get_domain('res/CascadiaMono-Bold.ttf'), 'CascadiaMono-Bold.ttf')
    download_resources("https://raw.githubusercontent.com/Sxvxgee/Darkend/main/Resources/trivia.json", 'trivia.json')
    t1 = Thread(target = infinite_check)
    t1.daemon = True
    t1.start()
  except:
    pass
  asyncio.run(asyncio.sleep(2.5))

  # App related stuff
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  make_dpi_aware() # has to be before app
  QtWidgets.QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough) # has to be before app
  font = QtGui.QFont("Century Gothic")
  app = QtWidgets.QApplication(sys.argv)
  app.aboutToQuit.connect(lambda: close_now())
  app.setAttribute(QtCore.Qt.AA_Use96Dpi)
  general_state, newlink_text, version_state = asyncio.run(version_check())

  if general_state is False:
    from utils.notifs import show_critical_messagebox
    if imported:
      pyi_splash.close()
    show_critical_messagebox('Couldn\'t establish an internet connection', 'Darkend can\'t function without proper WiFi.\nCheck your internet connection and try again.')
    sys.exit()
  
  if version_state is False:
    from utils.notifs import show_critical_messagebox
    if imported:
      pyi_splash.close()
    show_critical_messagebox('Old Version', f'<html><head/><body><p align=\"center\">There is a new version of Darkend released, use that one instead.<br>Download Link: <a href="{newlink_text}">Link</a></p></body></html>' if newlink_text is not None else '<html><head/><body><p align=\"center\">There is a new version of Darkend released, use that one instead.</a></p></body></html>')
    sys.exit()
  
  if general_state and version_state:
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_WelcomeWindow()
    ui.setupUi(MainWindow)
    icon = QtGui.QIcon(iconFromBase64(logo_b64))
    MainWindow.setWindowIcon(icon)
    MainWindow.setFixedSize(700, 300)
    MainWindow.setFont(font)
    MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    tray_icon = QtWidgets.QSystemTrayIcon()
    tray_icon.setIcon(iconFromBase64(logo_b64))
    shadow.internal["config"]['tray_icon'] = tray_icon
    tray_icon.show()
    MainWindow.show()
    if imported:
      pyi_splash.close()
    loop.run_forever()
    sys.exit(app.exec_())