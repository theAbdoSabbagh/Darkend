from PyQt5 import QtCore, QtGui, QtWidgets
from qasync import asyncSlot
from utils.useful import alt_scraper_html_text
from PyQt5.QtGui import QIntValidator
from utils.alt_handler_assist import create_account_file, update_account_settings, get_account_settings

import os, sys

# Paths
appdata = os.getenv('APPDATA')
directory = f"{appdata}\\Darkend v1"
gothic_century = f'{directory}\\Century Gothic.ttf'
gothic_century_bold = f'{directory}\\GOTHICB.TTF'
cascadia_mono = f'{directory}\\Cascadia Mono.ttf'

# Images
switch_on_b64 = b'iVBORw0KGgoAAAANSUhEUgAAAfQAAADICAMAAAApx+PaAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAACHUExURf38/SzKkCvIjy3Jjyi8hSvEjCrDiyzHjim+hirAiCvCif///yi5hCvFjSzGjQyGXSnBiSKWbF6oixzIiyOteyXJjt3y6ankyiW1gD3MlQF8UsTq2R6MZOv38USaelPQnojcuG3Uqhi+hI7BrCGjdHazm/b6+J3YvxbIiiDAhyq+h0q/kUdwTAcBqsMAAAAtdFJOU///////////////////////////////////////////////////////////AKXvC/0AABwPSURBVHja7J0JQ9s4E4YVyrYFsU0dYzvBzmFCJqF8///3ffIl65iRnJMu1tBjAcM2fvzOpZFg/ws2OmPhFgTowQL0YAF6sAA9WIAeLEAPFqAHC9CDBejBAvRgAXqwAD1YgB4sQA8WoAcL0IMF6AF6sAA9WIAeLEAPFqAHC9CDBejBAvRgAXqwLwN9N1utVlFRTIMNsJfepkURrWaz7X8L+na2alAX4p8fTLWi+qW81VbdqigSEpnVVmulxl+sroL+4tB3NW/x2t7enp+f5/P50/xJ2v3TCK26A3PCxC16/vgo91mepktgjFfGYJmmebYXrrJiH10cPLuswqP6mX0TsJ+Cdcwb7E8I7/lHmeXLBrWA3Vnznvi9THNxTwX41e4vhT4rKoUL4I47cF+9fXFzkdcUXmYpaLAt49UDsBTgheKj3V8HfSc0XljA70dr3ePdEpdqf2qZf2zyJc4bbPScpXvBfbra/k3QhciL6FkN362gfyJ2/+dLvzX2s0cvM5mG+dPz81OZg0oclF8ddzC483S7Epnd7m+BvhJx/O3ZkHeH+I+0hy9vfx76VyteePWAWw5fxPF9qmkcCKFrz0HFHfJd8VLM/gboNfK5SlzSfhifadx/NtifasnXWp/P1xm0xA2oBmzkMRC5XbqNXqazz4ZeIZeRvCOu4P6t2OOXt/olPz48Vq+/Q3//50+n9vm8zBkSyDv8Km5Qgfef4MsK++4zoc8q5DrxDvg4KKPkH3vdN9TFm5C6UHnOuA4R0KTdBK6H9+VWOPntZ0HfFrVjn7fIe+Ia7+/jsY5649ik2n9WUp+/fmSME3Bl5gZ6GqfpXj4pPN1N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'
switch_off_b64 = b'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'
double_left_b64 = b'iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAYAAAAehFoBAAADR0lEQVRYhe2ZzWsaQRjGn+YDEgo5leBJGtQEEXPKXYXS0mByacGKWG1vbYkp9NJe+hc05NTe7N1D8VBvpSWQS08tOXkyKBhDcog1fjSa6pQJOzI72ZldNTRZmgf24LDzzm9f34/ZWeBaV1+3ATwD8A1AVbs+A3gMwGHRxi0AjwB84mxsA0gBcF8k7EsAdQBEcv0C8MDExh0NUGajCeDtRcGeKhZi128ADyU27mpAZja6DPrGkLDrAN4BmGADCwsLiEaj6Ha7SKfTqFQq/P1lAH7N40z3tBC4yQYcDgcSiQSmp6eRzWaxs7PD2/ij2RhYKW1y3wOrq6uk2WwSpmq1SpaWlkQv3RdgdaHk9/tJpVLp2zg5OSGxWEy08WZQ2DXt75HCMh0dHZGZmRl+sY8yWJ/PR/b398/ZoNDCg/8YBPa5GFsrKyuGsEzJZJK//6cRrNfrJQcHB1Ibm5ubujUnLIAy2Pf8QDgcRiaTOYs3mWg8c3KJMev1erG1tYXZ2VmpjV6vZxFRD6t7yuXl5bO/S6VyuUwmJyelmW/mWapGo0E8Hg8/b9sMds0IttPpmMI6nU4pLI1ZM9h6vU4CgYA4N6WCTYkJRmHb7bZyoVKpRObm5qSwtBoYJRiv4+NjEgwGxbkdAE4Z7LpYuqx4tlgsEpfLJYVdXFzUlS4j1Wo1EgqFxLm0QSVksOc6WDgcNo3Z3d1d4na7lbB7e3vDwFLPJi3D0tLVarVMYYXkGBiWhoEBbBvAE1UY6GBlTYFXoVAg8/PzI8HSBDOIWQr7VJVgynYr86wKVmy3RqKly6AaKGFdw3jWLAxk7daCZzuqMKB6NUi7JVo1UCWYlaYggT1VJRjTd94rZglG66yqdE1NTQ0L21WVLl79SXSjoRLtYKqmQC+64VGJxqwBLL3iVmDHrNx01WS7kLBd0tmurMFujYPJVq2ZyVabHyn0Vd5e8uFhmw08k61ekZhs9RLKZKvXfCk0TUSz6hGPx/k5XwA0BoXe2NjQrWt18/MBwAt+IJfLIRKJoNVqSSeNj4/zP79qZ8UNNpDP5xEMBnF4eCi1MTY22v5slMPA15qNf3YYyHSpx63/xYE206V8MhhVtvoow2Srz17XMtNfelhrYWNTxT4AAAAASUVORK5CYII='
single_left_b64 = b'iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAYAAAAehFoBAAACL0lEQVRYhdWZTWoCMRiGX0s3urAHKAg6IgUPILQHsIgzR+hKEFr8gR6jC3fuuha39g7FIxTEGQW7KthuFP9KSmRC05iZ0er85IHAkBn1IX6Z70sCnA4NwCOAPgBit77dp53wd05CHcCaExXb2n4mEjQAbFxkWdvYz4ZKUxzZfD5PWq3WttFrQXoK4DIysrquk/l8Thj0mvYJ0ndhyDZEWcMwyGw2IyK0L5PJ8MIvQcvWxZh1kmU0m01e2ApStgbg+xBZSrVaDUX4Xpz5ND69ZEejEUkmk/znnkORLZfLfyaYjPF4TDRNEyfdbeCypVKJLBYLV9nJZELS6bQoOwFw4adsTSa7Wq08ZVOplCj7BeDaT9m6OMGo7HK59AwDych+ArjxU3Yn3e4zsnSCSWLWd9mdDEYnmFfMmqZJstms77IxiewTgHPWoes6ut0u4vG445dYloVisYjBYCDeegDweqTjB4B32Y290y3PcDgkuVzOq1I7pk1lVd7B6ZaFgc+yfGm6radj9mrgjQ8DwzDQ6XSQSCRc/6t2uy0Lg5PQ6/VgmibfRaWvYC9hDkq3QUAdJKUpdf1dg9GC2yvdBgl1ERYB/TMABTbmlUrF9W0QNNSFOnEUzsLT+T9KhQRUm3RKvtagUuLgUSI1K1388NKRLS+dUKqAZyi1RGIotQhlKLXMd5SO8kaKo3SUt6oYSm0GMpTabmUotaHNUOrIwFE6yocyDKWOvRhKHSwyAjm6/QEUWZwclR9NLwAAAABJRU5ErkJggg=='
double_right_b64 = b'iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAYAAAAehFoBAAADjElEQVRYhe2ZwUtUQRzHv+22IBIiERISS7KrtIh6ETy6ShTJKliBgWytedoiW6hDXfoPRDrUMfBkHjpEXiIKwUsdqkMH8bCioK4Kurn7dtddWydG3jzG55uZt6sFA/5gYPf3dr7z2Xm/+f3mzQNO7f9aEMAYgDkAabO9A3AHwAWXGhcB3AXwgdP4AiAO4PJJwr4AkANABI0OfFWhcQvAb4lGFkDipGDLkoFYo3/omkDjNoCCC42940B7AVwB8Nb8fGAdHR2Ix+Po6upCMpmEYRjskg/ATQDfASQ5nXoA7wGcZ47GxkYkEgn09vYilUpha2uLXfKYdyoD4Fs10M/5GRgeHia7u7uE2draGmlra3O6tdc5jRv89c7OTpJOpy2NXC5HBgYG7Bp/zPVSsf3gB+JhmaVSKdLa2iqDfsP8dXV1ZHt7+4iGAJqG4aNKgS2BiYmJIwMx29jYIKFQSAT9k/lisZhQg0L39/c7xfUDt7Ae/sv+/r7whw0NDZidnUUoFOLd58y0F2COcrks1KitrcX09DQikYj90qtKoOfYP21ubiaGYQhnSDLTVvP5fGRlZUWqQcOur6+v6pke4zt1d3eTbDarhHaIaav5/X4ldKlUEkErY9oPoMR3CofDJJPJSAekC9Ehe1itqamJLC8vSzWKxaITdNlN9rhnJnSrY09PD9nZ2ZEOSFNee3u7EDoQCJClpaVqZpqmvMcq6Jh9pt1Ar66uSqGDwSBZXFyUatCYjkQiVVXEEQBFO7QqPFTQdDGroPP5vFPKcwV93w5NY1q1EFXQLS0tJJlMSjUExWXPTXgcgabZQ5XyBGX8ELRqpo9TxkecsodqpgVlvKLwkMx0QAUds2cPN9Cq4kIXoip7CMr4ExUwzJRXrga6pqZGmvJUeZouRNvd+uoGmFrUPiCFVsU03QiJgFlxUVVEuiHj+3hcwGpnWoWEVotOq7SmVeHQqjRrtfnRanup1QZeu0ck7R5CtXvMtzqMj49XA0tPCj+x79FoVKpBs4HDAnMNe2jz4/GI90Kbm5sIh8OYn5/n3YZ5JvyZObxer2N/avl8HkNDQ5iZmbFfegjgtRtgnNBh4DPm/x+HgVodt54xD7R/ATjLnPRAe3BwEIVCAZOTk1hfX+f75Mww+Mj56k2NS8xBD7RHR0cPQmRqagoLCwu8BoV9CuBlpcDMtHllYIfW5qUMM61ee53av7C/58FtfR1a6wgAAAAASUVORK5CYII='
single_right_b64 = b'iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAYAAAAehFoBAAACJklEQVRYhdWZzWrCQBDH/y29eLGnngpCEpWCD1BoX6CI5ipeehIEoRoofQ576bEvoSffwEfoRavgue3F+FFly5Rsu435aG1MnD8MJEvC/hhmd2Z2gehkALgF0AcgHOs7Y0aE80SiJoB3BdRt7843e6EWgFUArLSV822iOgXwooIVCgXRbrc/jZ49PG0lCXytApXLZWHbtpCiZxrbJ+iuBNF1XUynU+EWjZmm6QWdSHg8SwjLsjZgQ6BXSSzEL+B6ve4LHAC9BnATJ/CjnDydTovRaBQK7RHTZI24gK/UiQ3DEOPxOBCaFmKpVEoM+hjARJ1Y0zQxmUwCoefzuSgWi4lBXwB4UyfOZDKh0Mvl0g86lpi+BPDq9nRYeCwWCy/odVy7xwY0xXTYQvTxdGxpfAM6m82K4XAYGtMeC9EzIx643qk2OPknNMX0gzqQy+XQ6/WgaZrvT7PZDJVKBd1uVx0mT98BuPf6p+UuZKK0fD4vBoNBoKf/ksabvywR/w0dFh5hafzA6QaeABxJel3XYZrmlhERLAqPRiN4u7VtG9VqFZ1ORx0m6DM4LcyPEtGr6opbPmmcWL97MCq41Xo2aRGLqwnoHwI4lz6v1WpIpVI7CYVtRCzEpOj8MDmc7cUqJMBt0bHc1sApcahikZpZFz9RaOfl5U5h97mAZ9UisWpC2bX57A5S2B1VsTsMZHfcyu5Am92VAbtLGXC79pJidbEoFcvV7QetFpQc67TqEgAAAABJRU5ErkJggg=='
arrow_back_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAASZJREFUaEPt19sNwjAMBVDfyViFbgIbwASUDdmgKFJBFUrSPPwqSr6b5h7bHwno4AsHz08DYN3B0YHRgc4KjBHKFXBZljMRnQBMnYVObhfrwBr+sZ48SyFEAD/hg+EJIHSDfbEDNMOHarACtMOzAizCswGswrMALMN3A6zDdwE8hG8GeAnfBPAUvhrgLXwVwGP4YkAk/IuIbuwXm8gPAVxz5+xeJSLhNXJ/zwCQzfj/gFCKxAjdNVoB4NI1Qp/NEYTYI6WmMLsjtP2ZR0QVIDFOpp2oBnhDNAE8IZoBXhBdAA+IboA1ggVgiWADWCFYARYIdoA2QgQQQUwA5po7Tum3YoANgqTCF7/ISqth8Z1oBzRAA6BRZZYXmXXQ1PljhKw7c/gOvAEHCJ4xH7xA5AAAAABJRU5ErkJggg=='

# Other
version = '0.4'

class PlainTextEdit(QtWidgets.QPlainTextEdit):
    def keyPressEvent(self, event):
      # if self.settings["config"]["autofarming"] is True:
        # return
      if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
          return
      super().keyPressEvent(event)

def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

class AltGUI(object):
    def __init__(self, account_id, tray_icon, messenger_):
        self.account_id = account_id
        create_account_file(self.account_id)
        self.settings = get_account_settings(account_id)
        self.internal = {"scraper_working" : False, "tray_icon": tray_icon, "MainWindow": None}
        
        # This way you don't overwrite data like autofarming
        self.messenger = messenger_

        # messenger internal does not have the account_id yet if alt gui was opened before initiating the autofarm
        try:
          fixing_purposes = self.messenger.internal[self.account_id]
        except:
          self.messenger.internal[self.account_id] = {"start_scraping": False, "scraper_pages": None, "scraper_working": False, "scraper_current_page": 0, "scraper_max_pages": 0, "scraper_last_page_item_amount": 0, "scraper_current_pages": 0,'autofarming': None, 'profile_data': None, "crash" : False}
        else:
          pass
        
        self.messenger.internal[self.account_id]["start_scraping"] = False
        self.messenger.internal[self.account_id]["scraper_pages"] = None
        self.messenger.internal[self.account_id]["scraper_working"] = False
        self.messenger.internal[self.account_id]["scraper_current_page"] = 0
        self.messenger.internal[self.account_id]["scraper_max_pages"] = 0
        self.messenger.internal[self.account_id]["scraper_last_page_item_amount"] = 0
        self.messenger.internal[self.account_id]["scraper_current_pages"] = 0
        self.messenger.internal[self.account_id]["profile_data"] = None

    def setupUi(self, MainWindow):
      QtWidgets.QPlainTextEdit = PlainTextEdit

      MainWindow.setObjectName("MainWindow")
      MainWindow.resize(996, 481)
      self.centralwidget = QtWidgets.QWidget(MainWindow)
      self.centralwidget.setObjectName("centralwidget")
      self._1_automation_frame = QtWidgets.QFrame(self.centralwidget)
      self._1_automation_frame.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      font.setBold(True)
      font.setWeight(75)
      self._1_automation_frame.setFont(font)
      self._1_automation_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
      self._1_automation_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._1_automation_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self._1_automation_frame.setObjectName("_1_automation_frame")
      self.automation_depositing = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_depositing.setGeometry(QtCore.QRect(20, 90, 221, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_depositing.setFont(font)
      self.automation_depositing.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_depositing.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_depositing.setIcon(iconFromBase64(switch_off_b64))
      self.automation_depositing.setIconSize(QtCore.QSize(75, 1000))
      self.automation_depositing.setObjectName("automation_depositing")
      self.automation_fishing = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_fishing.setGeometry(QtCore.QRect(20, 120, 181, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_fishing.setFont(font)
      self.automation_fishing.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_fishing.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_fishing.setIcon(iconFromBase64(switch_off_b64))
      self.automation_fishing.setIconSize(QtCore.QSize(75, 1000))
      self.automation_fishing.setObjectName("automation_fishing")
      self.automation_hunting = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_hunting.setGeometry(QtCore.QRect(20, 150, 191, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_hunting.setFont(font)
      self.automation_hunting.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_hunting.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_hunting.setIcon(iconFromBase64(switch_off_b64))
      self.automation_hunting.setIconSize(QtCore.QSize(75, 1000))
      self.automation_hunting.setObjectName("automation_hunting")
      self.automation_digging = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_digging.setGeometry(QtCore.QRect(20, 180, 191, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_digging.setFont(font)
      self.automation_digging.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_digging.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_digging.setIcon(iconFromBase64(switch_off_b64))
      self.automation_digging.setIconSize(QtCore.QSize(75, 1000))
      self.automation_digging.setObjectName("automation_digging")
      self.automation_title = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_title.setGeometry(QtCore.QRect(0, 0, 1001, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.automation_title.setFont(font)
      self.automation_title.setStyleSheet("")
      self.automation_title.setObjectName("automation_title")
      self.automation_highlow = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_highlow.setGeometry(QtCore.QRect(250, 150, 201, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_highlow.setFont(font)
      self.automation_highlow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_highlow.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_highlow.setIcon(iconFromBase64(switch_off_b64))
      self.automation_highlow.setIconSize(QtCore.QSize(75, 1000))
      self.automation_highlow.setObjectName("automation_highlow")
      self.automation_begging = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_begging.setGeometry(QtCore.QRect(20, 210, 201, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_begging.setFont(font)
      self.automation_begging.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_begging.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_begging.setIcon(iconFromBase64(switch_off_b64))
      self.automation_begging.setIconSize(QtCore.QSize(75, 1000))
      self.automation_begging.setObjectName("automation_begging")
      self.automation_premium_label = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_premium_label.setGeometry(QtCore.QRect(20, 270, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(19)
      self.automation_premium_label.setFont(font)
      self.automation_premium_label.setStyleSheet("border: 1px solid black\n"
      ";background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);")
      self.automation_premium_label.setObjectName("automation_premium_label")
      self.automation_premium_combo = QtWidgets.QComboBox(self._1_automation_frame)
      self.automation_premium_combo.setEnabled(True)
      self.automation_premium_combo.setGeometry(QtCore.QRect(250, 270, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      font.setBold(True)
      font.setWeight(75)
      self.automation_premium_combo.setFont(font)
      self.automation_premium_combo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_premium_combo.setStyleSheet("QComboBox {\n    background-color: rgb(255, 255, 255);\n    color:  rgb(27, 27, 27);\n    border: 2px solid rgb(27, 27, 27);\n}\n\nQComboBox::drop-down {\n    /*color: rgb(27, 27, 27);\n    background-color: rgb(27, 27, 27);*/\n    border: 0x;\n    border-radius: 0px;\n    border: 0px;\n}\nQComboBox::drop-down:button{\n    border-radius: 0px;\n}\n")
      self.automation_premium_combo.setEditable(False)
      self.automation_premium_combo.setDuplicatesEnabled(False)
      self.automation_premium_combo.setObjectName("automation_premium_combo")
      self.automation_premium_combo.addItem("Normie")
      self.automation_premium_combo.addItem("Donor")
      self.automation_presence_label = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_presence_label.setGeometry(QtCore.QRect(20, 320, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(19)
      self.automation_presence_label.setFont(font)
      self.automation_presence_label.setStyleSheet("border: 1px solid black\n"
      ";background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);")
      self.automation_presence_label.setObjectName("automation_presence_label")
      self.automation_meme = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_meme.setGeometry(QtCore.QRect(250, 120, 221, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_meme.setFont(font)
      self.automation_meme.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_meme.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_meme.setIcon(iconFromBase64(switch_off_b64))
      self.automation_meme.setIconSize(QtCore.QSize(75, 1000))
      self.automation_meme.setObjectName("automation_meme")
      self.automation_search = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_search.setGeometry(QtCore.QRect(250, 90, 191, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_search.setFont(font)
      self.automation_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_search.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_search.setIcon(iconFromBase64(switch_off_b64))
      self.automation_search.setIconSize(QtCore.QSize(75, 1000))
      self.automation_search.setObjectName("automation_search")
      self.automation_crime = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_crime.setGeometry(QtCore.QRect(250, 180, 181, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_crime.setFont(font)
      self.automation_crime.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_crime.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_crime.setIcon(iconFromBase64(switch_off_b64))
      self.automation_crime.setIconSize(QtCore.QSize(75, 1000))
      self.automation_crime.setObjectName("automation_crime")
      self.automation_trivia = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_trivia.setGeometry(QtCore.QRect(250, 210, 171, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_trivia.setFont(font)
      self.automation_trivia.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_trivia.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_trivia.setIcon(iconFromBase64(switch_off_b64))
      self.automation_trivia.setIconSize(QtCore.QSize(75, 1000))
      self.automation_trivia.setObjectName("automation_trivia")
      self.automation_presence_combo = QtWidgets.QComboBox(self._1_automation_frame)
      self.automation_presence_combo.setEnabled(True)
      self.automation_presence_combo.setGeometry(QtCore.QRect(250, 320, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      font.setBold(True)
      font.setWeight(75)
      self.automation_presence_combo.setFont(font)
      self.automation_presence_combo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_presence_combo.setStyleSheet("QComboBox {\n    background-color: rgb(255, 255, 255);\n    color:  rgb(27, 27, 27);\n    border: 2px solid rgb(27, 27, 27);\n}\n\nQComboBox::drop-down {\n    /*color: rgb(27, 27, 27);\n    background-color: rgb(27, 27, 27);*/\n    border: 0px;\n    border-radius: 0px;\n    border: 0px;\n}\nQComboBox::drop-down:button{\n    border-radius: 0px;\n}\n")
      self.automation_presence_combo.setEditable(False)
      self.automation_presence_combo.setDuplicatesEnabled(False)
      self.automation_presence_combo.setObjectName("automation_presence_combo")
      self.automation_presence_combo.addItem("Online")
      self.automation_presence_combo.addItem("DND (Do Not Disturb)")
      self.automation_presence_combo.addItem("Idle")
      self.automation_presence_combo.addItem("Invisible")
      self.automation_go_back = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_go_back.setGeometry(QtCore.QRect(840, 350, 121, 41))
      self.automation_go_back.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.automation_go_back.setFont(font)
      self.automation_go_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_go_back.setStyleSheet("QPushButton {\n"
      "    border: 0px;\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: rgb(255, 255, 255);\n"
      "    text-align: center;\n"
      "    border-radius: 10px;\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 15px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.automation_go_back.setIcon(iconFromBase64(arrow_back_b64))
      self.automation_go_back.setIconSize(QtCore.QSize(30, 1000))
      self.automation_go_back.setObjectName("go_back")
      self.automation_command_delay = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_command_delay.setGeometry(QtCore.QRect(710, 121, 221, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_command_delay.setFont(font)
      self.automation_command_delay.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_command_delay.setStyleSheet("QPushButton {\n    border-radius: 1px;\n    text-align: left;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      self.automation_command_delay.setIcon(iconFromBase64(switch_off_b64))
      self.automation_command_delay.setIconSize(QtCore.QSize(75, 1000))
      self.automation_command_delay.setObjectName("automation_command_delay")
      self.automation_dm_mode = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_dm_mode.setGeometry(QtCore.QRect(710, 150, 241, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_dm_mode.setFont(font)
      self.automation_dm_mode.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_dm_mode.setStyleSheet("QPushButton {\n    border-radius: 1px;\n    text-align: left;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      self.automation_dm_mode.setIcon(iconFromBase64(switch_off_b64))
      self.automation_dm_mode.setIconSize(QtCore.QSize(75, 1000))
      self.automation_dm_mode.setObjectName("automation_dm_mode")

      self.automation_snakeeyes = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_snakeeyes.setGeometry(QtCore.QRect(480, 120, 221, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_snakeeyes.setFont(font)
      self.automation_snakeeyes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_snakeeyes.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_snakeeyes.setIcon(iconFromBase64(switch_off_b64))
      self.automation_snakeeyes.setIconSize(QtCore.QSize(75, 1000))
      self.automation_snakeeyes.setObjectName("automation_snakeeyes")

      self.automation_work = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_work.setGeometry(QtCore.QRect(480, 90, 221, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_work.setFont(font)
      self.automation_work.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_work.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_work.setIcon(iconFromBase64(switch_off_b64))
      self.automation_work.setIconSize(QtCore.QSize(75, 1000))
      self.automation_work.setObjectName("automation_work")

      self.automation_gamble = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_gamble.setGeometry(QtCore.QRect(480, 210, 201, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_gamble.setFont(font)
      self.automation_gamble.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_gamble.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_gamble.setIcon(iconFromBase64(switch_off_b64))
      self.automation_gamble.setIconSize(QtCore.QSize(75, 1000))
      self.automation_gamble.setObjectName("automation_gamble")
      self.automation_scratch = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_scratch.setGeometry(QtCore.QRect(480, 150, 201, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_scratch.setFont(font)
      self.automation_scratch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_scratch.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_scratch.setIcon(iconFromBase64(switch_off_b64))
      self.automation_scratch.setIconSize(QtCore.QSize(75, 1000))
      self.automation_scratch.setObjectName("automation_scratch")
      self.automation_slots = QtWidgets.QPushButton(self._1_automation_frame)
      self.automation_slots.setGeometry(QtCore.QRect(480, 180, 181, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.automation_slots.setFont(font)
      self.automation_slots.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_slots.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.automation_slots.setIcon(iconFromBase64(switch_off_b64))
      self.automation_slots.setIconSize(QtCore.QSize(75, 1000))
      self.automation_slots.setObjectName("automation_slots")
      self.automation_slots_label = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_slots_label.setGeometry(QtCore.QRect(490, 270, 141, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(19)
      self.automation_slots_label.setFont(font)
      self.automation_slots_label.setStyleSheet("border: 1px solid black\n;background-color: rgb(27, 27, 27);\ncolor: rgb(255, 255, 255);")
      self.automation_slots_label.setObjectName("automation_slots_label")

      self.automation_job_label = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_job_label.setGeometry(QtCore.QRect(730, 270, 61, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(19)
      self.automation_job_label.setFont(font)
      self.automation_job_label.setStyleSheet("border: 1px solid black\n;background-color: rgb(27, 27, 27);\ncolor: rgb(255, 255, 255);")
      self.automation_job_label.setObjectName("automation_job_label")
      self.automation_job_combo = QtWidgets.QComboBox(self._1_automation_frame)
      self.automation_job_combo.setEnabled(True)
      self.automation_job_combo.setGeometry(QtCore.QRect(790, 270, 191, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      font.setBold(True)
      font.setWeight(75)
      self.automation_job_combo.setFont(font)
      self.automation_job_combo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.automation_job_combo.setStyleSheet("QComboBox {\n    background-color: rgb(255, 255, 255);\n    color:  rgb(27, 27, 27);\n    border: 2px solid rgb(27, 27, 27);\n}\n\nQComboBox::drop-down {\n    /*color: rgb(27, 27, 27);\n    background-color: rgb(27, 27, 27);*/\n    border: 0x;\n    border-radius: 0px;\n    border: 0px;\n}\nQComboBox::drop-down:button{\n    border-radius: 0px; border: 0px;\n}\n")
      self.automation_job_combo.setEditable(False)
      self.automation_job_combo.setDuplicatesEnabled(False)
      self.automation_job_combo.setObjectName("automation_job_combo")
      _jobs = ["Automatic", "Discord Mod", "Babysitter", "Fast Food Cook", "House Wife", "Twitch Streamer", "YouTuber", "Professional Hunter", "Professional Fisherman", "Bartender", "Robber", "Police Officer", "Teacher", "Musician", "Pro Gamer", "Manager", "Developer", "Day Trader", "Santa Claus", "Politician", "Veterinarian", "Pharmacist", "Dank Memer Shopkeeper", "Lawyer", "Doctor", "Scientist", "Ghost"]
      for _job in _jobs:
        self.automation_job_combo.addItem(_job)
      self.automation_scratch_label = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_scratch_label.setGeometry(QtCore.QRect(490, 320, 141, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(19)
      self.automation_scratch_label.setFont(font)
      self.automation_scratch_label.setStyleSheet("border: 1px solid black\n;background-color: rgb(27, 27, 27);\ncolor: rgb(255, 255, 255);")
      self.automation_scratch_label.setObjectName("automation_scratch_label")
      self.automation_gamble_label = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_gamble_label.setGeometry(QtCore.QRect(490, 370, 141, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(19)
      self.automation_gamble_label.setFont(font)
      self.automation_gamble_label.setStyleSheet("border: 1px solid black\n;background-color: rgb(27, 27, 27);\ncolor: rgb(255, 255, 255);")
      self.automation_gamble_label.setObjectName("automation_gamble_label")
      self.automation_snakeeyes_label = QtWidgets.QLabel(self._1_automation_frame)
      self.automation_snakeeyes_label.setGeometry(QtCore.QRect(490, 420, 141, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(19)
      self.automation_snakeeyes_label.setFont(font)
      self.automation_snakeeyes_label.setStyleSheet("border: 1px solid black\n;background-color: rgb(27, 27, 27);\ncolor: rgb(255, 255, 255);")
      self.automation_snakeeyes_label.setObjectName("automation_snakeeyes_label")
      self.automation_scratch_input = QtWidgets.QLineEdit(self._1_automation_frame)
      self.automation_scratch_input.setGeometry(QtCore.QRect(630, 320, 91, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.automation_scratch_input.setFont(font)
      self.automation_scratch_input.setToolTip("<html><head/><body><p align=\"center\">Cannot be lesser than 1,500 or more than 250,000</p></body></html>")
      self.automation_scratch_input.setToolTipDuration(1999999999)
      self.automation_scratch_input.setStyleSheet("QLineEdit {\n    border: 2px solid rgb(27, 27, 27);\n    text-align: center;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      self.automation_scratch_input.setAlignment(QtCore.Qt.AlignCenter)
      self.automation_scratch_input.setObjectName("automation_scratch_input")
      self.automation_slots_input = QtWidgets.QLineEdit(self._1_automation_frame)
      self.automation_slots_input.setGeometry(QtCore.QRect(630, 270, 91, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.automation_slots_input.setFont(font)
      self.automation_slots_input.setToolTip("<html><head/><body><p align=\"center\">Cannot be more than 2,000</p></body></html>")
      self.automation_slots_input.setToolTipDuration(1999999999)
      self.automation_slots_input.setStyleSheet("QLineEdit {\n    border: 2px solid rgb(27, 27, 27);\n    text-align: center;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      self.automation_slots_input.setInputMethodHints(QtCore.Qt.ImhNone)
      self.automation_slots_input.setEchoMode(QtWidgets.QLineEdit.Normal)
      self.automation_slots_input.setAlignment(QtCore.Qt.AlignCenter)
      self.automation_slots_input.setClearButtonEnabled(False)
      self.automation_slots_input.setObjectName("automation_slots_input")
      self.automation_gamble_input = QtWidgets.QLineEdit(self._1_automation_frame)
      self.automation_gamble_input.setGeometry(QtCore.QRect(630, 370, 91, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.automation_gamble_input.setFont(font)
      self.automation_gamble_input.setToolTip("<html><head/><body><p align=\"center\">Cannot be lesser than 1,500 or more than 250,000</p></body></html>")
      self.automation_gamble_input.setToolTipDuration(1999999999)
      self.automation_gamble_input.setStyleSheet("QLineEdit {\n"
      "    border: 2px solid rgb(27, 27, 27);\n"
      "    text-align: center;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.automation_gamble_input.setAlignment(QtCore.Qt.AlignCenter)
      self.automation_gamble_input.setObjectName("automation_gamble_input")
      self.automation_snakeeyes_input = QtWidgets.QLineEdit(self._1_automation_frame)
      self.automation_snakeeyes_input.setGeometry(QtCore.QRect(630, 420, 91, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.automation_snakeeyes_input.setFont(font)
      self.automation_snakeeyes_input.setToolTip("<html><head/><body><p align=\"center\">Cannot be lesser than 1,500 or more than 250,000</p></body></html>")
      self.automation_snakeeyes_input.setToolTipDuration(1999999999)
      self.automation_snakeeyes_input.setStyleSheet("QLineEdit {\n"
      "    border: 2px solid rgb(27, 27, 27);\n"
      "    text-align: center;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.automation_snakeeyes_input.setAlignment(QtCore.Qt.AlignCenter)
      self.automation_snakeeyes_input.setObjectName("automation_snakeeyes_input")
      self.automation_title.raise_()
      self.automation_digging.raise_()
      self.automation_hunting.raise_()
      self.automation_fishing.raise_()
      self.automation_begging.raise_()
      self.automation_premium_combo.raise_()
      self.automation_presence_label.raise_()
      self.automation_meme.raise_()
      self.automation_crime.raise_()
      self.automation_trivia.raise_()
      self.automation_presence_combo.raise_()
      self.automation_search.raise_()
      self.automation_depositing.raise_()
      self.automation_premium_label.raise_()
      self.automation_highlow.raise_()
      self.automation_go_back.raise_()
      self.automation_dm_mode.raise_()
      self.automation_command_delay.raise_()
      self.automation_snakeeyes.raise_()
      self.automation_work.raise_()
      self.automation_gamble.raise_()
      self.automation_scratch.raise_()
      self.automation_slots.raise_()
      self.automation_slots_label.raise_()
      self.automation_scratch_label.raise_()
      self.automation_gamble_label.raise_()
      self.automation_snakeeyes_label.raise_()
      self.automation_scratch_input.raise_()
      self.automation_slots_input.raise_()
      self.automation_gamble_input.raise_()
      self.automation_snakeeyes_input.raise_()
      self._2_inventory_scraper = QtWidgets.QFrame(self.centralwidget)
      self._2_inventory_scraper.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
      self._2_inventory_scraper.setStyleSheet("QFrame {\n"
      "    background-color: rgb(255, 255, 255);\n"
      "}\n"
      "QScrollBar:vertical {\n"
      " }\n"
      "QScrollBar::add-line:vertical {\n"
      "      border: none;\n"
      "      background: none;\n"
      "}\n"
      "\n"
      "QScrollBar::sub-line:vertical {\n"
      "      border: none;\n"
      "      background: none;\n"
      "}\n"
      "\n"
      "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
      "      border: none;\n"
      "      background: none;\n"
      "}\n"
      "\n"
      "QScrollBar:horizontal {\n"
      " }\n"
      "QScrollBar::add-line:horizontal {\n"
      "      border: none;\n"
      "      background: none;\n"
      "}\n"
      "\n"
      "QScrollBar::sub-line:horizontal {\n"
      "      border: none;\n"
      "      background: none;\n"
      "}\n"
      "\n"
      "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
      "      border: none;\n"
      "      background: none;\n"
      "}")
      self._2_inventory_scraper.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._2_inventory_scraper.setFrameShadow(QtWidgets.QFrame.Raised)
      self._2_inventory_scraper.setObjectName("_2_inventory_scraper")
      self.scraper_title = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_title.setGeometry(QtCore.QRect(0, 0, 991, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.scraper_title.setFont(font)
      self.scraper_title.setStyleSheet("")
      self.scraper_title.setObjectName("scraper_title")
      self.scraper_inventory = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_inventory.setGeometry(QtCore.QRect(740, 80, 231, 291))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_inventory.setFont(font)
      self.scraper_inventory.setStyleSheet("border: 2px solid  rgb(27, 27, 27);\n"
      "/*border-radius: 10px;*/\n"
      "qproperty-alignment: AlignTop;\n"
      "padding-left: 5px;\n"
      "padding-right: 5px;\n"
      "padding-top: 5px;")
      self.scraper_inventory.setWordWrap(True)
      self.scraper_inventory.setObjectName("scraper_inventory")
      self.scraper_double_right_arrow = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_double_right_arrow.setGeometry(QtCore.QRect(920, 420, 51, 41))
      self.scraper_double_right_arrow.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_double_right_arrow.setFont(font)
      self.scraper_double_right_arrow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_double_right_arrow.setStyleSheet("QPushButton {\n"
      "    background-color: rgb(66,69,73);\n"
      "    border-radius: 5px;\n"
      "    text-align: center;\n"
      "}\n"
      "QPushButton:hover {\n"
      "    background-color: rgb(54,57,62);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    background-color: rgb(40,43,48);\n"
      "}\n"
      "")
      self.scraper_double_right_arrow.setText("")
      self.scraper_double_right_arrow.setIcon(iconFromBase64(double_right_b64))
      self.scraper_double_right_arrow.setIconSize(QtCore.QSize(30, 1000))
      self.scraper_double_right_arrow.setObjectName("scraper_double_right_arrow")
      self.scraper_double_left_arrow = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_double_left_arrow.setGeometry(QtCore.QRect(740, 420, 51, 41))
      self.scraper_double_left_arrow.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_double_left_arrow.setFont(font)
      self.scraper_double_left_arrow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_double_left_arrow.setStyleSheet("QPushButton {\n"
      "    background-color: rgb(66,69,73);\n"
      "    border-radius: 5px;\n"
      "    text-align: center;\n"
      "}\n"
      "QPushButton:hover {\n"
      "    background-color: rgb(54,57,62);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    background-color: rgb(40,43,48);\n"
      "}\n"
      "")
      self.scraper_double_left_arrow.setText("")
      self.scraper_double_left_arrow.setIcon(iconFromBase64(double_left_b64))
      self.scraper_double_left_arrow.setIconSize(QtCore.QSize(30, 1000))
      self.scraper_double_left_arrow.setObjectName("scraper_double_left_arrow")
      self.scraper_left_arrow = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_left_arrow.setGeometry(QtCore.QRect(800, 420, 51, 41))
      self.scraper_left_arrow.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_left_arrow.setFont(font)
      self.scraper_left_arrow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_left_arrow.setStyleSheet("QPushButton {\n"
      "    background-color: rgb(66,69,73);\n"
      "    border-radius: 5px;\n"
      "    text-align: center;\n"
      "}\n"
      "QPushButton:hover {\n"
      "    background-color: rgb(54,57,62);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    background-color: rgb(40,43,48);\n"
      "}\n"
      "")
      self.scraper_left_arrow.setText("")
      self.scraper_left_arrow.setIcon(iconFromBase64(single_left_b64))
      self.scraper_left_arrow.setIconSize(QtCore.QSize(30, 1000))
      self.scraper_left_arrow.setObjectName("scraper_left_arrow")
      self.scraper_right_arrow = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_right_arrow.setGeometry(QtCore.QRect(860, 420, 51, 41))
      self.scraper_right_arrow.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_right_arrow.setFont(font)
      self.scraper_right_arrow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_right_arrow.setStyleSheet("QPushButton {\n"
      "    background-color: rgb(66,69,73);\n"
      "    border-radius: 5px;\n"
      "    text-align: center;\n"
      "}\n"
      "QPushButton:hover {\n"
      "    background-color: rgb(54,57,62);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    background-color: rgb(40,43,48);\n"
      "}\n"
      "")
      self.scraper_right_arrow.setText("")
      self.scraper_right_arrow.setIcon(iconFromBase64(single_right_b64))
      self.scraper_right_arrow.setIconSize(QtCore.QSize(30, 1000))
      self.scraper_right_arrow.setObjectName("scraper_right_arrow")
      self.scraper_scrollArea = QtWidgets.QScrollArea(self._2_inventory_scraper)
      self.scraper_scrollArea.setGeometry(QtCore.QRect(10, 250, 471, 201))
      self.scraper_scrollArea.setMinimumSize(QtCore.QSize(0, 0))
      self.scraper_scrollArea.setStyleSheet("border: none;")
      self.scraper_scrollArea.setWidgetResizable(True)
      self.scraper_scrollArea.setObjectName("scraper_scrollArea")
      self.scraper_scroll_widget = QtWidgets.QWidget()
      self.scraper_scroll_widget.setGeometry(QtCore.QRect(0, 0, 454, 1218))
      self.scraper_scroll_widget.setStyleSheet("background-color: rgb(12, 12, 12);\n"
      "border: 1px solid white;")
      self.scraper_scroll_widget.setObjectName("scraper_scroll_widget")
      self.verticalLayout = QtWidgets.QVBoxLayout(self.scraper_scroll_widget)
      self.verticalLayout.setObjectName("verticalLayout")
      self.scraper_frame = QtWidgets.QFrame(self.scraper_scroll_widget)
      self.scraper_frame.setMinimumSize(QtCore.QSize(0, 1200))
      self.scraper_frame.setStyleSheet("background-color: rgb(12, 12, 12);\n"
      "border: none;")
      self.scraper_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.scraper_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self.scraper_frame.setObjectName("scraper_frame")
      self.scraper_holder = QtWidgets.QLabel(self.scraper_frame)
      self.scraper_holder.setGeometry(QtCore.QRect(0, 0, 16777215, 16777215))
      font = QtGui.QFont()
      font.setFamily("Cascadia Mono")
      font.setPixelSize(13)
      self.scraper_holder.setFont(font)
      self.scraper_holder.setStyleSheet("border:  2px solid rgb(12, 12, 12);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "qproperty-alignment: AlignTop;\n"
      "background-color: rgb(12, 12, 12);")
      self.scraper_holder.setObjectName("scraper_holder")
      self.verticalLayout.addWidget(self.scraper_frame)
      self.scraper_scrollArea.setWidget(self.scraper_scroll_widget)
      self.scraper_refresh_button = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_refresh_button.setGeometry(QtCore.QRect(10, 190, 151, 41))
      self.scraper_refresh_button.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_refresh_button.setFont(font)
      self.scraper_refresh_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_refresh_button.setStyleSheet("QPushButton {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: rgb(255, 255, 255);\n"
      "    border-radius: 5px;\n"
      "    text-align: center;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 15px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.scraper_refresh_button.setIconSize(QtCore.QSize(30, 1000))
      self.scraper_refresh_button.setObjectName("scraper_refresh_button")
      self.scraper_resume_autofarm = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_resume_autofarm.setGeometry(QtCore.QRect(10, 140, 381, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_resume_autofarm.setFont(font)
      self.scraper_resume_autofarm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_resume_autofarm.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.scraper_resume_autofarm.setIcon(iconFromBase64(switch_off_b64))
      self.scraper_resume_autofarm.setIconSize(QtCore.QSize(75, 1000))
      self.scraper_resume_autofarm.setObjectName("scraper_resume_autofarm")
      self.scraper_retry_success = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_retry_success.setGeometry(QtCore.QRect(10, 110, 291, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_retry_success.setFont(font)
      self.scraper_retry_success.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_retry_success.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.scraper_retry_success.setIcon(iconFromBase64(switch_off_b64))
      self.scraper_retry_success.setIconSize(QtCore.QSize(75, 1000))
      self.scraper_retry_success.setObjectName("scraper_retry_success")
      self.scraper_alert = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_alert.setGeometry(QtCore.QRect(10, 80, 211, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.scraper_alert.setFont(font)
      self.scraper_alert.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_alert.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.scraper_alert.setIcon(iconFromBase64(switch_off_b64))
      self.scraper_alert.setIconSize(QtCore.QSize(75, 1000))
      self.scraper_alert.setObjectName("scraper_alert")
      self.scraper_currently_viewing = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_currently_viewing.setGeometry(QtCore.QRect(740, 380, 231, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_currently_viewing.setFont(font)
      self.scraper_currently_viewing.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_currently_viewing.setObjectName("scraper_currently_viewing")
      self.scraper_go_back = QtWidgets.QPushButton(self._2_inventory_scraper)
      self.scraper_go_back.setGeometry(QtCore.QRect(170, 190, 121, 41))
      self.scraper_go_back.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.scraper_go_back.setFont(font)
      self.scraper_go_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.scraper_go_back.setStyleSheet("QPushButton {\n"
      "    border: 0px;\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: rgb(255, 255, 255);\n"
      "    text-align: center;\n"
      "    border-radius: 10px;\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 15px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.scraper_go_back.setIcon(iconFromBase64(arrow_back_b64))
      self.scraper_go_back.setIconSize(QtCore.QSize(30, 1000))
      self.scraper_go_back.setObjectName("scraper_go_back")
      self.scraper_unique_items = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_unique_items.setGeometry(QtCore.QRect(500, 280, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_unique_items.setFont(font)
      self.scraper_unique_items.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_unique_items.setObjectName("scraper_unique_items")
      self.scraper_bot_balance = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_bot_balance.setGeometry(QtCore.QRect(500, 130, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_bot_balance.setFont(font)
      self.scraper_bot_balance.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_bot_balance.setObjectName("scraper_bot_balance")
      self.scraper_bot_bank = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_bot_bank.setGeometry(QtCore.QRect(500, 180, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_bot_bank.setFont(font)
      self.scraper_bot_bank.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_bot_bank.setObjectName("scraper_bot_bank")
      self.scraper_bot_level = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_bot_level.setGeometry(QtCore.QRect(500, 230, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_bot_level.setFont(font)
      self.scraper_bot_level.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_bot_level.setObjectName("scraper_bot_level")
      self.scraper_total_items = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_total_items.setGeometry(QtCore.QRect(500, 330, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_total_items.setFont(font)
      self.scraper_total_items.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_total_items.setObjectName("scraper_total_items")
      self.scraper_total_commands = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_total_commands.setGeometry(QtCore.QRect(500, 380, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_total_commands.setFont(font)
      self.scraper_total_commands.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_total_commands.setObjectName("scraper_total_commands")
      self.scraper_bot_networth = QtWidgets.QLabel(self._2_inventory_scraper)
      self.scraper_bot_networth.setGeometry(QtCore.QRect(500, 80, 231, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.scraper_bot_networth.setFont(font)
      self.scraper_bot_networth.setStyleSheet("background-color: rgb(66,69,73);\n"
      "border-radius: 5px;\n"
      "padding-top: 1px;\n"
      "color: white;")
      self.scraper_bot_networth.setObjectName("scraper_bot_networth")
      self._3_powerups_frame = QtWidgets.QFrame(self.centralwidget)
      self._3_powerups_frame.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
      self._3_powerups_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
      self._3_powerups_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._3_powerups_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self._3_powerups_frame.setObjectName("_3_powerups_frame")
      self.powerups_title = QtWidgets.QLabel(self._3_powerups_frame)
      self.powerups_title.setGeometry(QtCore.QRect(0, 0, 1001, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.powerups_title.setFont(font)
      self.powerups_title.setStyleSheet("")
      self.powerups_title.setObjectName("powerups_title")
      self.powerups_ammo = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_ammo.setGeometry(QtCore.QRect(30, 200, 211, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_ammo.setFont(font)
      self.powerups_ammo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_ammo.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_ammo.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_ammo.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_ammo.setObjectName("powerups_ammo")
      self.powerups_alcohol = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_alcohol.setGeometry(QtCore.QRect(30, 250, 211, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_alcohol.setFont(font)
      self.powerups_alcohol.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_alcohol.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_alcohol.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_alcohol.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_alcohol.setObjectName("powerups_alcohol")
      self.powerups_pizza = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_pizza.setGeometry(QtCore.QRect(30, 100, 211, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_pizza.setFont(font)
      self.powerups_pizza.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_pizza.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_pizza.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_pizza.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_pizza.setObjectName("powerups_pizza")
      self.powerups_apple = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_apple.setGeometry(QtCore.QRect(30, 150, 211, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_apple.setFont(font)
      self.powerups_apple.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_apple.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_apple.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_apple.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_apple.setObjectName("powerups_apple")
      self.powerups_reset_button = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_reset_button.setGeometry(QtCore.QRect(400, 340, 191, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_reset_button.setFont(font)
      self.powerups_reset_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_reset_button.setStyleSheet("QPushButton {\n"
      "background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 15px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.powerups_reset_button.setObjectName("powerups_reset_button")
      self.powerups_go_back = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_go_back.setGeometry(QtCore.QRect(430, 400, 131, 41))
      self.powerups_go_back.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_go_back.setFont(font)
      self.powerups_go_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_go_back.setStyleSheet("QPushButton {\n"
      "    border: 0px;\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: rgb(255, 255, 255);\n"
      "    text-align: center;\n"
      "    border-radius: 10px;\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 15px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.powerups_go_back.setIcon(iconFromBase64(arrow_back_b64))
      self.powerups_go_back.setIconSize(QtCore.QSize(30, 1000))
      self.powerups_go_back.setObjectName("powerups_go_back")
      self.powerups_prestige_coin = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_prestige_coin.setGeometry(QtCore.QRect(330, 200, 251, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_prestige_coin.setFont(font)
      self.powerups_prestige_coin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_prestige_coin.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_prestige_coin.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_prestige_coin.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_prestige_coin.setObjectName("powerups_prestige_coin")
      self.powerups_fishing_bait = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_fishing_bait.setGeometry(QtCore.QRect(330, 150, 251, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_fishing_bait.setFont(font)
      self.powerups_fishing_bait.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_fishing_bait.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_fishing_bait.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_fishing_bait.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_fishing_bait.setObjectName("powerups_fishing_bait")
      self.powerups_robbers_mask = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_robbers_mask.setGeometry(QtCore.QRect(330, 250, 251, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_robbers_mask.setFont(font)
      self.powerups_robbers_mask.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_robbers_mask.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_robbers_mask.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_robbers_mask.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_robbers_mask.setObjectName("powerups_robbers_mask")
      self.powerups_alcohol_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_alcohol_amount.setGeometry(QtCore.QRect(240, 250, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_alcohol_amount.setFont(font)
      self.powerups_alcohol_amount.setToolTipDuration(999999999)
      self.powerups_alcohol_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_alcohol_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_alcohol_amount.setObjectName("powerups_alcohol_amount")
      self.powerups_taco = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_taco.setGeometry(QtCore.QRect(670, 100, 221, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_taco.setFont(font)
      self.powerups_taco.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_taco.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_taco.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_taco.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_taco.setObjectName("powerups_taco")
      self.powerups_whiskey = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_whiskey.setGeometry(QtCore.QRect(670, 150, 221, 41))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(False); font.setWeight(50)
      self.powerups_whiskey.setFont(font)
      self.powerups_whiskey.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_whiskey.setStyleSheet("border: 2px solid rgb(27, 27, 27);\ntext-align: left;\nborder-right: 0px;\nborder-top-left-radius: 10px;\nborder-bottom-left-radius: 10px;")
      self.powerups_whiskey.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_whiskey.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_whiskey.setObjectName("powerups_whiskey")

      self.powerups_horseshoe = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_horseshoe.setGeometry(QtCore.QRect(670, 200, 221, 41))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(False); font.setWeight(50)
      self.powerups_horseshoe.setFont(font)
      self.powerups_horseshoe.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_horseshoe.setStyleSheet("border: 2px solid rgb(27, 27, 27);\ntext-align: left;\nborder-right: 0px;\nborder-top-left-radius: 10px;\nborder-bottom-left-radius: 10px;")
      self.powerups_horseshoe.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_horseshoe.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_horseshoe.setObjectName("powerups_horseshoe")
      self.powerups_horseshoe_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_horseshoe_amount.setGeometry(QtCore.QRect(890, 200, 71, 41))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(75); 
      self.powerups_horseshoe_amount.setFont(font)
      self.powerups_horseshoe_amount.setToolTipDuration(999999999)
      self.powerups_horseshoe_amount.setStyleSheet("QLineEdit {\n    border:2px solid rgb(27, 27, 27);\n    border-top-right-radius: 10px;\n    border-bottom-right-radius: 10px;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      self.powerups_horseshoe_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_horseshoe_amount.setObjectName("powerups_horseshoe_amount")

      self.powerups_cowboy_boots = QtWidgets.QPushButton(self._3_powerups_frame)
      self.powerups_cowboy_boots.setGeometry(QtCore.QRect(330, 100, 251, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.powerups_cowboy_boots.setFont(font)
      self.powerups_cowboy_boots.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.powerups_cowboy_boots.setStyleSheet("border: 2px solid rgb(27, 27, 27);\n"
      "text-align: left;\n"
      "border-right: 0px;\n"
      "border-top-left-radius: 10px;\n"
      "border-bottom-left-radius: 10px;")
      self.powerups_cowboy_boots.setIcon(iconFromBase64(switch_off_b64))
      self.powerups_cowboy_boots.setIconSize(QtCore.QSize(75, 1000))
      self.powerups_cowboy_boots.setObjectName("powerups_cowboy_boots")
      self.powerups_pizza_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_pizza_amount.setGeometry(QtCore.QRect(240, 100, 71, 41))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(75); 
      self.powerups_pizza_amount.setFont(font)
      self.powerups_pizza_amount.setToolTipDuration(999999999)
      self.powerups_pizza_amount.setStyleSheet("QLineEdit {\n    border:2px solid rgb(27, 27, 27);\n    border-top-right-radius: 10px;\n    border-bottom-right-radius: 10px;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      self.powerups_pizza_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_pizza_amount.setObjectName("powerups_pizza_amount")
      self.powerups_apple_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_apple_amount.setGeometry(QtCore.QRect(240, 150, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_apple_amount.setFont(font)
      self.powerups_apple_amount.setToolTipDuration(999999999)
      self.powerups_apple_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_apple_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_apple_amount.setObjectName("powerups_apple_amount")
      self.powerups_ammo_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_ammo_amount.setGeometry(QtCore.QRect(240, 200, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_ammo_amount.setFont(font)
      self.powerups_ammo_amount.setToolTipDuration(999999999)
      self.powerups_ammo_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_ammo_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_ammo_amount.setObjectName("powerups_ammo_amount")
      self.powerups_robbers_mask_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_robbers_mask_amount.setGeometry(QtCore.QRect(580, 250, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_robbers_mask_amount.setFont(font)
      self.powerups_robbers_mask_amount.setToolTipDuration(999999999)
      self.powerups_robbers_mask_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_robbers_mask_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_robbers_mask_amount.setObjectName("powerups_robbers_mask_amount")
      self.powerups_fishing_bait_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_fishing_bait_amount.setGeometry(QtCore.QRect(580, 150, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_fishing_bait_amount.setFont(font)
      self.powerups_fishing_bait_amount.setToolTipDuration(999999999)
      self.powerups_fishing_bait_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_fishing_bait_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_fishing_bait_amount.setObjectName("powerups_fishing_bait_amount")
      self.powerups_prestige_coin_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_prestige_coin_amount.setGeometry(QtCore.QRect(580, 200, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_prestige_coin_amount.setFont(font)
      self.powerups_prestige_coin_amount.setToolTipDuration(999999999)
      self.powerups_prestige_coin_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_prestige_coin_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_prestige_coin_amount.setObjectName("powerups_prestige_coin_amount")
      self.powerups_cowboy_boots_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_cowboy_boots_amount.setGeometry(QtCore.QRect(580, 100, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_cowboy_boots_amount.setFont(font)
      self.powerups_cowboy_boots_amount.setToolTipDuration(999999999)
      self.powerups_cowboy_boots_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_cowboy_boots_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_cowboy_boots_amount.setObjectName("powerups_cowboy_boots_amount")
      self.powerups_taco_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_taco_amount.setGeometry(QtCore.QRect(890, 100, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_taco_amount.setFont(font)
      self.powerups_taco_amount.setToolTipDuration(999999999)
      self.powerups_taco_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_taco_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_taco_amount.setObjectName("powerups_taco_amount")
      self.powerups_whiskey_amount = QtWidgets.QLineEdit(self._3_powerups_frame)
      self.powerups_whiskey_amount.setGeometry(QtCore.QRect(890, 150, 71, 41))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.powerups_whiskey_amount.setFont(font)
      self.powerups_whiskey_amount.setToolTipDuration(999999999)
      self.powerups_whiskey_amount.setStyleSheet("QLineEdit {\n"
      "    border:2px solid rgb(27, 27, 27);\n"
      "    border-top-right-radius: 10px;\n"
      "    border-bottom-right-radius: 10px;\n"
      "}\n"
      "QToolTip {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: white;\n"
      "    text-align: cetner;\n"
      "    border: 2px solid black;\n"
      "    font-family: Century Gothic;\n"
      "}")
      self.powerups_whiskey_amount.setAlignment(QtCore.Qt.AlignCenter)
      self.powerups_whiskey_amount.setObjectName("powerups_whiskey_amount")
      self._4_switcher_frame = QtWidgets.QFrame(self.centralwidget)
      self._4_switcher_frame.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
      self._4_switcher_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
      self._4_switcher_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._4_switcher_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self._4_switcher_frame.setObjectName("_4_switcher_frame")
      self.switcher_automation_view = QtWidgets.QPushButton(self._4_switcher_frame)
      self.switcher_automation_view.setGeometry(QtCore.QRect(40, 190, 231, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(24)
      font.setBold(False)
      font.setWeight(50)
      self.switcher_automation_view.setFont(font)
      self.switcher_automation_view.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.switcher_automation_view.setStyleSheet("QPushButton {\n"
      "background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 23px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.switcher_automation_view.setObjectName("switcher_automation_view")
      self.switcher_scraper_view = QtWidgets.QPushButton(self._4_switcher_frame)
      self.switcher_scraper_view.setGeometry(QtCore.QRect(380, 190, 231, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(24)
      font.setBold(False)
      font.setWeight(50)
      self.switcher_scraper_view.setFont(font)
      self.switcher_scraper_view.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.switcher_scraper_view.setStyleSheet("QPushButton {\n"
      "background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 23px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.switcher_scraper_view.setObjectName("switcher_scraper_view")
      self.switcher_autopowerups_view = QtWidgets.QPushButton(self._4_switcher_frame)
      self.switcher_autopowerups_view.setGeometry(QtCore.QRect(40, 370, 231, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(24)
      font.setBold(False)
      font.setWeight(50)
      self.switcher_autopowerups_view.setFont(font)
      self.switcher_autopowerups_view.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.switcher_autopowerups_view.setStyleSheet("QPushButton {\n"
      "background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 23px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.switcher_autopowerups_view.setObjectName("switcher_autopowerups_view")
      self.switcher_customization_view = QtWidgets.QPushButton(self._4_switcher_frame)
      self.switcher_customization_view.setGeometry(QtCore.QRect(380, 370, 231, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(24)
      font.setBold(False)
      font.setWeight(50)
      self.switcher_customization_view.setFont(font)
      self.switcher_customization_view.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.switcher_customization_view.setStyleSheet("QPushButton {\n"
      "background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 23px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.switcher_customization_view.setObjectName("switcher_customization_view")
      self.switcher_title = QtWidgets.QLabel(self._4_switcher_frame)
      self.switcher_title.setGeometry(QtCore.QRect(0, 0, 981, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.switcher_title.setFont(font)
      self.switcher_title.setStyleSheet("")
      self.switcher_title.setObjectName("switcher_title")
      self.switcher_automation_info = QtWidgets.QLabel(self._4_switcher_frame)
      self.switcher_automation_info.setGeometry(QtCore.QRect(40, 100, 231, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(37)
      self.switcher_automation_info.setFont(font)
      self.switcher_automation_info.setStyleSheet("border: 0px solid black;")
      self.switcher_automation_info.setObjectName("switcher_automation_info")
      self.switcher_scraper_info = QtWidgets.QLabel(self._4_switcher_frame)
      self.switcher_scraper_info.setGeometry(QtCore.QRect(380, 100, 231, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(37)
      self.switcher_scraper_info.setFont(font)
      self.switcher_scraper_info.setStyleSheet("border: 0px solid black;")
      self.switcher_scraper_info.setObjectName("switcher_scraper_info")
      self.switcher_autopowerups_info = QtWidgets.QLabel(self._4_switcher_frame)
      self.switcher_autopowerups_info.setGeometry(QtCore.QRect(40, 280, 231, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(37)
      self.switcher_autopowerups_info.setFont(font)
      self.switcher_autopowerups_info.setStyleSheet("border: 0px solid black;")
      self.switcher_autopowerups_info.setObjectName("switcher_autopowerups_info")
      self.switcher_customization_info = QtWidgets.QLabel(self._4_switcher_frame)
      self.switcher_customization_info.setGeometry(QtCore.QRect(380, 280, 231, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(37)
      self.switcher_customization_info.setFont(font)
      self.switcher_customization_info.setStyleSheet("border: 0px solid black;")
      self.switcher_customization_info.setObjectName("switcher_customization_info")
      self.switcher_ultimate_view = QtWidgets.QPushButton(self._4_switcher_frame)
      self.switcher_ultimate_view.setGeometry(QtCore.QRect(720, 190, 231, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(24)
      font.setBold(False)
      font.setWeight(50)
      self.switcher_ultimate_view.setFont(font)
      self.switcher_ultimate_view.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.switcher_ultimate_view.setStyleSheet("QPushButton {\n"
      "background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 23px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.switcher_ultimate_view.setObjectName("switcher_ultimate_view")
      self.switcher_ultimate_info = QtWidgets.QLabel(self._4_switcher_frame)
      self.switcher_ultimate_info.setGeometry(QtCore.QRect(720, 100, 231, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(37)
      self.switcher_ultimate_info.setFont(font)
      self.switcher_ultimate_info.setStyleSheet("border: 0px solid black;")
      self.switcher_ultimate_info.setObjectName("switcher_ultimate_info")
      self.switcher_coming_soon_info = QtWidgets.QLabel(self._4_switcher_frame)
      self.switcher_coming_soon_info.setGeometry(QtCore.QRect(720, 280, 231, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(37)
      self.switcher_coming_soon_info.setFont(font)
      self.switcher_coming_soon_info.setStyleSheet("border: 0px solid black;")
      self.switcher_coming_soon_info.setObjectName("switcher_coming_soon_info")
      self.switcher_coming_soon_view = QtWidgets.QPushButton(self._4_switcher_frame)
      self.switcher_coming_soon_view.setGeometry(QtCore.QRect(720, 370, 231, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(24)
      font.setBold(False)
      font.setWeight(50)
      self.switcher_coming_soon_view.setFont(font)
      self.switcher_coming_soon_view.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.switcher_coming_soon_view.setStyleSheet("QPushButton {\n"
      "background-color: rgb(27, 27, 27);\n"
      "color: rgb(255, 255, 255);\n"
      "border-radius: 10px;\n"
      "\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 23px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.switcher_coming_soon_view.setObjectName("switcher_coming_soon_view")
      self.switcher_automation_view.raise_()
      self.switcher_scraper_view.raise_()
      self.switcher_autopowerups_view.raise_()
      self.switcher_title.raise_()
      self.switcher_automation_info.raise_()
      self.switcher_scraper_info.raise_()
      self.switcher_autopowerups_info.raise_()
      self.switcher_customization_info.raise_()
      self.switcher_customization_view.raise_()
      self.switcher_ultimate_view.raise_()
      self.switcher_ultimate_info.raise_()
      self.switcher_coming_soon_info.raise_()
      self.switcher_coming_soon_view.raise_()
      self._5_customization_frame = QtWidgets.QFrame(self.centralwidget)
      self._5_customization_frame.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
      self._5_customization_frame.setStyleSheet("QFrame {\n"
      "    background-color: rgb(255, 255, 255);\n"
      "}\n"
      " QScrollBar:vertical {\n"
      "    color: white;\n"
      "    border: none;\n"
      "    background-color: none;\n"
      "    width: 10px;\n"
      "    margin: 15px 0 15px 0;\n"
      "    border-radius: 0px;\n"
      " }\n"
      "\n"
      "/*  HANDLE BAR VERTICAL */\n"
      "QScrollBar::handle:vertical {\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    min-height: 15px;\n"
      "    border-radius: 5px;\n"
      "}\n"
      "QScrollBar::handle:vertical:hover{    \n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QScrollBar::handle:vertical:pressed {    \n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "\n"
      "/* BTN TOP - SCROLLBAR */\n"
      "QScrollBar::sub-line:vertical {\n"
      "    border: none;\n"
      "    background-color:none;\n"
      "}\n"
      "\n"
      "/* BTN BOTTOM - SCROLLBAR */\n"
      "QScrollBar::add-line:vertical {\n"
      "    border: none;\n"
      "    background-color:none;\n"
      "}\n"
      "/* RESET ARROW */\n"
      "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
      "    background: none;\n"
      "}\n"
      "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
      "    background: white;\n"
      "}")
      self._5_customization_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._5_customization_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self._5_customization_frame.setObjectName("_5_customization_frame")
      self.customization_title = QtWidgets.QLabel(self._5_customization_frame)
      self.customization_title.setGeometry(QtCore.QRect(0, 0, 1001, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.customization_title.setFont(font)
      self.customization_title.setStyleSheet("")
      self.customization_title.setObjectName("customization_title")
      self.customization_hooks = QtWidgets.QLabel(self._5_customization_frame)
      self.customization_hooks.setGeometry(QtCore.QRect(10, 60, 291, 61))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(35)
      self.customization_hooks.setFont(font)
      self.customization_hooks.setStyleSheet("")
      self.customization_hooks.setObjectName("customization_hooks")
      self.customization_other_opt3 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_other_opt3.setGeometry(QtCore.QRect(320, 180, 211, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_other_opt3.setFont(font)
      self.customization_other_opt3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_other_opt3.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_other_opt3.setIcon(iconFromBase64(switch_off_b64))
      self.customization_other_opt3.setIconSize(QtCore.QSize(75, 1000))
      self.customization_other_opt3.setObjectName("customization_other_opt3")
      self.customization_other_opt2 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_other_opt2.setGeometry(QtCore.QRect(320, 150, 241, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_other_opt2.setFont(font)
      self.customization_other_opt2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_other_opt2.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_other_opt2.setIcon(iconFromBase64(switch_off_b64))
      self.customization_other_opt2.setIconSize(QtCore.QSize(75, 1000))
      self.customization_other_opt2.setObjectName("customization_other_opt2")
      self.customization_hooks_opt5 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt5.setGeometry(QtCore.QRect(10, 240, 221, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt5.setFont(font)
      self.customization_hooks_opt5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt5.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt5.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt5.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt5.setObjectName("customization_hooks_opt5")
      self.customization_hooks_opt1 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt1.setGeometry(QtCore.QRect(10, 120, 301, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt1.setFont(font)
      self.customization_hooks_opt1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt1.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt1.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt1.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt1.setObjectName("customization_hooks_opt1")
      self.customization_hooks_opt2 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt2.setGeometry(QtCore.QRect(10, 150, 271, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt2.setFont(font)
      self.customization_hooks_opt2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt2.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt2.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt2.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt2.setObjectName("customization_hooks_opt2")
      self.customization_hooks_opt9 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt9.setGeometry(QtCore.QRect(10, 360, 241, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt9.setFont(font)
      self.customization_hooks_opt9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt9.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt9.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt9.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt9.setObjectName("customization_hooks_opt9")
      self.customization_other = QtWidgets.QLabel(self._5_customization_frame)
      self.customization_other.setGeometry(QtCore.QRect(320, 60, 241, 61))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(35)
      self.customization_other.setFont(font)
      self.customization_other.setStyleSheet("")
      self.customization_other.setObjectName("customization_other")
      self.customization_hooks_opt6 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt6.setGeometry(QtCore.QRect(10, 270, 221, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt6.setFont(font)
      self.customization_hooks_opt6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt6.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt6.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt6.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt6.setObjectName("customization_hooks_opt6")
      self.customization_hooks_opt7 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt7.setGeometry(QtCore.QRect(10, 300, 201, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt7.setFont(font)
      self.customization_hooks_opt7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt7.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt7.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt7.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt7.setObjectName("customization_hooks_opt7")
      self.customization_hooks_opt8 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt8.setGeometry(QtCore.QRect(10, 330, 201, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt8.setFont(font)
      self.customization_hooks_opt8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt8.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt8.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt8.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt8.setObjectName("customization_hooks_opt8")
      self.customization_main_search_list = QtWidgets.QListWidget(self._5_customization_frame)
      self.customization_main_search_list.setGeometry(QtCore.QRect(790, 130, 161, 211))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.customization_main_search_list.setFont(font)
      self.customization_main_search_list.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_main_search_list.setMouseTracking(False)
      self.customization_main_search_list.setStyleSheet("QListWidget {\n"
      "    border: 2px solid rgb(27, 27, 27);\n"
      "    border-radius: 25px;\n"
      "    border-left: white;\n"
      "    border-right: white;\n"
      "    padding-top: 10px;\n"
      "    padding-bottom: 5px;\n"
      "    padding-left: 15px;\n"
      "}\n"
      "QListWidget::item:hover {\n"
      "    color: rgb(59, 59, 59);\n"
      "    background-color: white;\n"
      "}\n"
      "QListWidget::item:selected {\n"
      "    background-color: rgb(59, 59, 59);\n"
      "    color: white;\n"
      "}")
      self.customization_main_search_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
      self.customization_main_search_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.customization_main_search_list.setDragEnabled(False)
      self.customization_main_search_list.setDragDropOverwriteMode(False)
      self.customization_main_search_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
      self.customization_main_search_list.setProperty("isWrapping", False)
      self.customization_main_search_list.setWordWrap(True)
      self.customization_main_search_list.setSelectionRectVisible(False)
      self.customization_main_search_list.setObjectName("customization_main_search_list")
      item = QtWidgets.QListWidgetItem()
      item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
      item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
      self.customization_main_search = QtWidgets.QLabel(self._5_customization_frame)
      self.customization_main_search.setGeometry(QtCore.QRect(770, 70, 211, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(35)
      self.customization_main_search.setFont(font)
      self.customization_main_search.setStyleSheet("")
      self.customization_main_search.setObjectName("customization_main_search")
      self.customization_main_crime = QtWidgets.QLabel(self._5_customization_frame)
      self.customization_main_crime.setGeometry(QtCore.QRect(560, 70, 211, 51))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(35)
      self.customization_main_crime.setFont(font)
      self.customization_main_crime.setStyleSheet("")
      self.customization_main_crime.setObjectName("customization_main_crime")
      self.customization_main_crime_list = QtWidgets.QListWidget(self._5_customization_frame)
      self.customization_main_crime_list.setGeometry(QtCore.QRect(580, 130, 171, 211))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.customization_main_crime_list.setFont(font)
      self.customization_main_crime_list.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_main_crime_list.setStyleSheet("QListWidget {\n"
      "    border: 2px solid rgb(27, 27, 27);\n"
      "    border-radius: 25px;\n"
      "    border-left: white;\n"
      "    border-right: white;\n"
      "    padding-top: 10px;\n"
      "    padding-bottom: 5px;\n"
      "    padding-left: 15px;\n"
      "    padding-right: 15px;\n"
      "}\n"
      "QListWidget::item:hover {\n"
      "    color: rgb(59, 59, 59);\n"
      "    background-color: white;\n"
      "}\n"
      "QListWidget::item:selected {\n"
      "    background-color: rgb(59, 59, 59);\n"
      "    color: white;\n"
      "}")
      self.customization_main_crime_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
      self.customization_main_crime_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.customization_main_crime_list.setDragEnabled(False)
      self.customization_main_crime_list.setDragDropOverwriteMode(False)
      self.customization_main_crime_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
      self.customization_main_crime_list.setProperty("isWrapping", False)
      self.customization_main_crime_list.setWordWrap(True)
      self.customization_main_crime_list.setSelectionRectVisible(False)
      self.customization_main_crime_list.setObjectName("customization_main_crime_list")
      self.customization_hooks_opt4 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt4.setGeometry(QtCore.QRect(10, 210, 231, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt4.setFont(font)
      self.customization_hooks_opt4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt4.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt4.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt4.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt4.setObjectName("customization_hooks_opt4")
      self.customization_go_back = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_go_back.setGeometry(QtCore.QRect(40, 410, 121, 41))
      self.customization_go_back.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.customization_go_back.setFont(font)
      self.customization_go_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_go_back.setStyleSheet("QPushButton {\n"
      "    border: 0px;\n"
      "    background-color: rgb(27, 27, 27);\n"
      "    color: rgb(255, 255, 255);\n"
      "    text-align: center;\n"
      "    border-radius: 10px;\n"
      "}\n"
      "QPushButton::hover{\n"
      "    background-color: rgb(59, 59, 59);\n"
      "}\n"
      "QPushButton:pressed {\n"
      "    font-size: 15px;\n"
      "    font-family: Century Gothic;\n"
      "    background-color: rgb(43, 43, 43);\n"
      "}\n"
      "")
      self.customization_go_back.setIcon(iconFromBase64(arrow_back_b64))
      self.customization_go_back.setIconSize(QtCore.QSize(30, 1000))
      self.customization_go_back.setObjectName("customization_go_back")
      self.customization_hooks_opt3 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_hooks_opt3.setGeometry(QtCore.QRect(10, 180, 251, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_hooks_opt3.setFont(font)
      self.customization_hooks_opt3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_hooks_opt3.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_hooks_opt3.setIcon(iconFromBase64(switch_off_b64))
      self.customization_hooks_opt3.setIconSize(QtCore.QSize(75, 1000))
      self.customization_hooks_opt3.setObjectName("customization_hooks_opt3")
      self.customization_other_opt4 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_other_opt4.setGeometry(QtCore.QRect(320, 210, 181, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_other_opt4.setFont(font)
      self.customization_other_opt4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_other_opt4.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_other_opt4.setIcon(iconFromBase64(switch_off_b64))
      self.customization_other_opt4.setIconSize(QtCore.QSize(75, 1000))
      self.customization_other_opt4.setObjectName("customization_other_opt4")
      self.customization_other_opt1 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_other_opt1.setGeometry(QtCore.QRect(320, 120, 241, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_other_opt1.setFont(font)
      self.customization_other_opt1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_other_opt1.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_other_opt1.setIcon(iconFromBase64(switch_off_b64))
      self.customization_other_opt1.setIconSize(QtCore.QSize(75, 1000))
      self.customization_other_opt1.setObjectName("customization_other_opt1")
      self.customization_other_opt5 = QtWidgets.QPushButton(self._5_customization_frame)
      self.customization_other_opt5.setGeometry(QtCore.QRect(320, 240, 171, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(False)
      font.setWeight(50)
      self.customization_other_opt5.setFont(font)
      self.customization_other_opt5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.customization_other_opt5.setStyleSheet("border-radius: 1px;\n"
      "text-align: left;")
      self.customization_other_opt5.setIcon(iconFromBase64(switch_off_b64))
      self.customization_other_opt5.setIconSize(QtCore.QSize(75, 1000))
      self.customization_other_opt5.setObjectName("customization_other_opt5")
      self.customization_hooks.raise_()
      self.customization_other.raise_()
      self.customization_other_opt2.raise_()
      self.customization_other_opt3.raise_()
      self.customization_hooks_opt6.raise_()
      self.customization_hooks_opt5.raise_()
      self.customization_hooks_opt2.raise_()
      self.customization_hooks_opt3.raise_()
      self.customization_title.raise_()
      self.customization_hooks_opt9.raise_()
      self.customization_hooks_opt7.raise_()
      self.customization_hooks_opt8.raise_()
      self.customization_main_search.raise_()
      self.customization_main_crime.raise_()
      self.customization_main_crime_list.raise_()
      self.customization_main_search_list.raise_()
      self.customization_hooks_opt4.raise_()
      self.customization_go_back.raise_()
      self.customization_hooks_opt1.raise_()
      self.customization_hooks_opt3.raise_()
      self.customization_other_opt4.raise_()
      self.customization_other_opt1.raise_()
      self.customization_other_opt5.raise_()
      self._0_coming_soon = QtWidgets.QFrame(self.centralwidget)
      self._0_coming_soon.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
      self._0_coming_soon.setStyleSheet("background-color: rgba(90, 90, 90, 200);")
      self._0_coming_soon.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._0_coming_soon.setFrameShadow(QtWidgets.QFrame.Raised)
      self._0_coming_soon.setObjectName("_0_coming_soon")
      self.coming_soon_title = QtWidgets.QLabel(self._0_coming_soon)
      self.coming_soon_title.setGeometry(QtCore.QRect(0, 180, 1001, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.coming_soon_title.setFont(font)
      self.coming_soon_title.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
      "color: white;")
      self.coming_soon_title.setObjectName("coming_soon_title")

      # Scraper Assist Frame
      self._0_scraper_assist = QtWidgets.QFrame(self.centralwidget)
      self._0_scraper_assist.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
      self._0_scraper_assist.setStyleSheet("background-color: rgba(90, 90, 90, 200);")
      self._0_scraper_assist.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._0_scraper_assist.setFrameShadow(QtWidgets.QFrame.Raised)
      self._0_scraper_assist.setObjectName("_0_scraper_assist")

      self.scraper_assist_title = QtWidgets.QLabel(self._0_scraper_assist)
      self.scraper_assist_title.setGeometry(QtCore.QRect(0, 180, 991, 71))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.scraper_assist_title.setFont(font)
      self.scraper_assist_title.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
      self.scraper_assist_title.setObjectName("scraper_assist_title")

      self._0_coming_soon.raise_()
      self._2_inventory_scraper.raise_()
      self._3_powerups_frame.raise_()
      self._1_automation_frame.raise_()
      self._5_customization_frame.raise_()
      self._4_switcher_frame.raise_()
      MainWindow.setCentralWidget(self.centralwidget)
      self.retranslateUi(MainWindow)

      # Disabled
      self.automation_dm_mode.setDisabled(True)

      # Go back
      self.automation_go_back.clicked.connect(lambda: self.switch_frame(self._4_switcher_frame))
      self.powerups_go_back.clicked.connect(lambda: self.switch_frame(self._4_switcher_frame))
      self.scraper_go_back.clicked.connect(lambda: self.switch_frame(self._4_switcher_frame))
      self.customization_go_back.clicked.connect(lambda: self.switch_frame(self._4_switcher_frame))

      # Lists
      self.customization_main_search_list.itemClicked.connect(self.search_places)
      self.customization_main_crime_list.itemClicked.connect(self.crime_actions)

      # Switcher
      self.switcher_automation_view.clicked.connect(lambda: self.switch_frame(self._1_automation_frame))
      self.switcher_scraper_view.clicked.connect(lambda: self.switch_frame(self._2_inventory_scraper))
      self.switcher_autopowerups_view.clicked.connect(lambda: self.switch_frame(self._3_powerups_frame))
      self.switcher_customization_view.clicked.connect(lambda: self.switch_frame(self._5_customization_frame))

      # Effects
      buttons_list = [
        self.switcher_automation_view,
        self.switcher_scraper_view,
        self.switcher_autopowerups_view,
        self.switcher_customization_view,
        self.scraper_refresh_button,
        self.automation_go_back,
        self.powerups_go_back,
        self.scraper_go_back,
        self.customization_go_back,
        self.switcher_ultimate_view,
        self.switcher_coming_soon_view,
        self.powerups_reset_button,
      ]
      for item in buttons_list:
        effect = QtWidgets.QGraphicsDropShadowEffect(item)
        effect.setOffset(0, 0)
        effect.setColor(QtGui.QColor(43, 43, 43))
        effect.setBlurRadius(30)
        item.setGraphicsEffect(effect)

      # Automation Buttons
      self.automation_depositing.clicked.connect(lambda: self.automation_change_icon(self.automation_depositing, 'auto_dep'))
      self.automation_highlow.clicked.connect(lambda: self.automation_change_icon(self.automation_highlow, 'auto_highlow'))
      self.automation_begging.clicked.connect(lambda: self.automation_change_icon(self.automation_begging, 'auto_beg'))
      self.automation_fishing.clicked.connect(lambda: self.automation_change_icon(self.automation_fishing, 'auto_fish'))
      self.automation_hunting.clicked.connect(lambda: self.automation_change_icon(self.automation_hunting, 'auto_hunt'))
      self.automation_digging.clicked.connect(lambda: self.automation_change_icon(self.automation_digging, 'auto_dig'))
      self.automation_search.clicked.connect(lambda: self.automation_change_icon(self.automation_search, 'auto_search'))
      self.automation_trivia.clicked.connect(lambda: self.automation_change_icon(self.automation_trivia, 'auto_trivia'))
      self.automation_crime.clicked.connect(lambda: self.automation_change_icon(self.automation_crime, 'auto_crime'))
      self.automation_meme.clicked.connect(lambda: self.automation_change_icon(self.automation_meme, 'auto_meme'))
      self.automation_command_delay.clicked.connect(lambda: self.automation_change_icon(self.automation_command_delay, 'command_delay'))
      self.automation_dm_mode.clicked.connect(lambda: self.automation_change_icon(self.automation_dm_mode, 'dm_mode'))
      self.automation_slots.clicked.connect(lambda: self.automation_change_icon(self.automation_slots, 'slots'))
      self.automation_scratch.clicked.connect(lambda: self.automation_change_icon(self.automation_scratch, 'scratch'))
      self.automation_gamble.clicked.connect(lambda: self.automation_change_icon(self.automation_gamble, 'gamble'))
      self.automation_snakeeyes.clicked.connect(lambda: self.automation_change_icon(self.automation_snakeeyes, 'snakeeyes'))
      self.automation_work.clicked.connect(lambda: self.automation_change_icon(self.automation_work, 'work'))

      # Powerups
      self.powerups_pizza.clicked.connect(lambda: self.powerups_change_icon(self.powerups_pizza, 'pizza'))
      self.powerups_whiskey.clicked.connect(lambda: self.powerups_change_icon(self.powerups_whiskey, 'whiskey'))
      self.powerups_horseshoe.clicked.connect(lambda: self.powerups_change_icon(self.powerups_horseshoe, 'horseshoe'))
      self.powerups_ammo.clicked.connect(lambda: self.powerups_change_icon(self.powerups_ammo, 'ammo'))
      self.powerups_alcohol.clicked.connect(lambda: self.powerups_change_icon(self.powerups_alcohol, 'alcohol'))
      self.powerups_apple.clicked.connect(lambda: self.powerups_change_icon(self.powerups_apple, 'apple'))
      self.powerups_taco.clicked.connect(lambda: self.powerups_change_icon(self.powerups_taco, 'taco'))
      self.powerups_fishing_bait.clicked.connect(lambda: self.powerups_change_icon(self.powerups_fishing_bait, 'fishingbait'))
      self.powerups_prestige_coin.clicked.connect(lambda: self.powerups_change_icon(self.powerups_prestige_coin, 'prestige'))
      self.powerups_robbers_mask.clicked.connect(lambda: self.powerups_change_icon(self.powerups_robbers_mask, 'robbersmask'))
      self.powerups_cowboy_boots.clicked.connect(lambda: self.powerups_change_icon(self.powerups_cowboy_boots, 'boots'))
      self.powerups_reset_button.clicked.connect(lambda: self.reset_quantities())

      # customization
      self.customization_hooks_opt1.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt1, 'autofarm_logging'))
      self.customization_hooks_opt2.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt2, 'powerup_logging'))
      self.customization_hooks_opt3.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt3, 'event_sniping_logging'))
      self.customization_hooks_opt4.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt4, 'autotool_logging'))
      self.customization_hooks_opt5.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt5, 'autobuy_logging'))
      self.customization_hooks_opt6.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt6, 'levelup_logging'))
      self.customization_hooks_opt7.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt7, 'death_logging'))
      self.customization_hooks_opt8.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt8, 'work_logging'))
      self.customization_hooks_opt9.clicked.connect(lambda: self.customization_change_icon(self.customization_hooks_opt9, 'timestamps_logging'))

      self.customization_other_opt1.clicked.connect(lambda: self.customization_change_icon(self.customization_other_opt1, 'autobuypowerups'))
      self.customization_other_opt2.clicked.connect(lambda: self.customization_change_icon(self.customization_other_opt2, 'deathlifesaver'))
      self.customization_other_opt3.clicked.connect(lambda: self.customization_change_icon(self.customization_other_opt3, 'withdraw'))
      self.customization_other_opt4.clicked.connect(lambda: self.customization_change_icon(self.customization_other_opt4, 'embed_hooks'))
      self.customization_other_opt5.clicked.connect(lambda: self.customization_change_icon(self.customization_other_opt5, 'autotool'))
      
      # Scraper Buttons
      self.scraper_refresh_button.clicked.connect(lambda: self.scrape_inventory())
      self.scraper_alert.clicked.connect(lambda: self.automation_change_icon(self.scraper_alert, 'scraper_alert'))
      self.scraper_retry_success.clicked.connect(lambda: self.automation_change_icon(self.scraper_retry_success, 'scraper_retry'))
      self.scraper_resume_autofarm.clicked.connect(lambda: self.automation_change_icon(self.scraper_resume_autofarm, 'resume_after_scraping'))
      self.scraper_double_left_arrow.setEnabled(False)
      self.scraper_left_arrow.setEnabled(False)
      self.scraper_right_arrow.setEnabled(False)
      self.scraper_double_right_arrow.setEnabled(False)
      self.scraper_double_left_arrow.clicked.connect(lambda: self.scraper_max_back())
      self.scraper_double_right_arrow.clicked.connect(lambda: self.scraper_max_next())
      self.scraper_left_arrow.clicked.connect(lambda: self.scraper_back())
      self.scraper_right_arrow.clicked.connect(lambda: self.scraper_next())

      # Comboboxes
      self.automation_premium_combo.currentTextChanged.connect(lambda: self.set_combo_values(self.automation_premium_combo))
      self.automation_presence_combo.currentTextChanged.connect(lambda: self.set_combo_values(self.automation_presence_combo))
      self.automation_job_combo.currentTextChanged.connect(lambda: self.set_combo_values(self.automation_job_combo))

      # LineEdits
      self.powerups_pizza_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_pizza_amount, 'pizza_amount'))
      self.powerups_whiskey_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_whiskey_amount, 'whiskey_amount'))
      self.powerups_horseshoe_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_horseshoe_amount, 'horseshoe_amount'))
      self.powerups_alcohol_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_alcohol_amount, 'alcohol_amount'))
      self.powerups_ammo_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_ammo_amount, 'ammo_amount'))
      self.powerups_taco_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_taco_amount, 'taco_amount'))
      self.powerups_fishing_bait_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_fishing_bait_amount, 'fishingbait_amount'))
      self.powerups_apple_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_apple_amount, 'apple_amount'))
      self.powerups_prestige_coin_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_prestige_coin_amount, 'prestige_amount'))
      self.powerups_robbers_mask_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_robbers_mask_amount, 'robbersmask_amount'))
      self.powerups_cowboy_boots_amount.textChanged.connect(lambda: self.update_powerups_amount(self.powerups_cowboy_boots_amount, 'boots_amount'))
      
      self.automation_slots_input.textChanged.connect(lambda: self.update_bet(self.automation_slots_input, 'slots_bet', min_ = 1, max_ = 2000))
      self.automation_scratch_input.textChanged.connect(lambda: self.update_bet(self.automation_scratch_input, 'scratch_bet', min_ = 1500, max_ = 250000))
      self.automation_gamble_input.textChanged.connect(lambda: self.update_bet(self.automation_gamble_input, 'gamble_bet', min_ = 1500, max_ = 250000))
      self.automation_snakeeyes_input.textChanged.connect(lambda: self.update_bet(self.automation_snakeeyes_input, 'snakeeyes_bet', min_ = 1500, max_ = 250000))

      # Essential
      self.essential()
      self.pre_select_items()

      QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def reset_quantities(self):
      from utils.notifs import critical_messagebox_multi_gui, notification_messagebox_multi_gui
      self.settings = get_account_settings(self.account_id)

      powerup_amount_data = [
      'pizza_amount', 'boots_amount', 'ammo_amount', 
      'alcohol_amount', 'fidget_amount', 'apple_amount', 
      'taco_amount', 'fishingbait_amount', 'prestige_amount', 
      'robbersmask_amount', 'whiskey_amount', 
      ]
      for property_ in powerup_amount_data:
        self.settings['powerups'][property_] = 0

      powerup_name_data = [
      'pizza', 'boots', 'ammo', 
      'alcohol', 'fidget', 'apple', 
      'taco', 'fishingbait', 'prestige', 
      'robbersmask', 'whiskey', 
      ]
      for property_ in powerup_name_data:
        self.settings['powerups'][property_] = False
      
      self.essential()
      notification_messagebox_multi_gui(self.internal['tray_icon'], "Powerups resetted", 'The powerups data has been resetted back to default.')
      return update_account_settings(self.account_id, self.settings)

    def update_bet(self, item : QtWidgets.QLineEdit, property : str, /, min_ : int, max_ : int):
      self.settings = get_account_settings(self.account_id)
      amount = ''.join(c for c in item.text() if c.isdigit())
      
      if len(str(amount)) == 0:
        amount = 0
      amount = int(amount)
      
      if amount < min_:
        amount = min_
      if amount > max_:
        amount = max_

      item.setText(str(amount))

      self.settings["config"][property] = int(amount)
      
      update_account_settings(self.account_id, self.settings)

    def update_powerups_amount(self, item : QtWidgets.QLineEdit, property : str):
      self.settings = get_account_settings(self.account_id)
      amount = ''.join(c for c in item.text() if c.isdigit())
      item.setText(amount)

      if len(amount) == 0:
        self.settings["powerups"][property] = 0
        item.setText('0')
      else:
        self.settings["powerups"][property] = int(amount)
      
      update_account_settings(self.account_id, self.settings)

    @asyncSlot()
    async def scrape_inventory(self):
      import asyncio
      from utils.notifs import critical_messagebox_multi_gui, notification_messagebox_multi_gui
      from utils.useful import unique_items_html, bot_balance_html, bot_bank_html, bot_level_html, total_items_html, total_commands_html, networth_html

      # Checking if autofarming was ever started first
      if self.messenger.internal[self.account_id]['autofarming'] is None:
        return critical_messagebox_multi_gui(self.internal['tray_icon'], "Invalid autofarming session", 'You must start the bot at least once in order to use this feature. You could also use it when autofarming is paused.')
      
      self.settings = get_account_settings(self.account_id)
      # Cleaning data
      self.messenger.internal[self.account_id]["start_scraping"] = False
      self.messenger.internal[self.account_id]["scraper_pages"] = 0
      self.messenger.internal[self.account_id]["scraper_working"] = False
      self.messenger.internal[self.account_id]["scraper_current_page"] = 0
      self.messenger.internal[self.account_id]["scraper_max_pages"] = 0
      self.messenger.internal[self.account_id]["scraper_last_page_item_amount"] = 0
      self.messenger.internal[self.account_id]["profile_data"] = None

      notification_messagebox_multi_gui(self.internal['tray_icon'], "Starting Inventory Scraper", 'Autofarming has been paused.')
      self.messenger.internal[self.account_id]['autofarming'] = False
      self.change_terminal_text("Scraping inventory...")

      # Shows "Hold on..."
      if self.internal['current_frame'] == self._2_inventory_scraper:
        self._0_scraper_assist.raise_()
        self.scraper_assist_title.show()

      # Waits a bit so commands are over
      await asyncio.sleep(5)
      self.messenger.internal[self.account_id]["start_scraping"] = True
      
      while True:
        # Waiting until the scraper is done
        if self.messenger.internal[self.account_id]["start_scraping"] is True:
          await asyncio.sleep(0.55)
          continue
        
        # Text setting
        self.scraper_inventory.setText(self.messenger.internal[self.account_id]['scraper_pages'][0])
        self.change_terminal_text("Scraped inventory successfully.", newline = True)
        
        # Hiding the assist stuff and updating the frame and all
        if self.internal['current_frame'] == self._2_inventory_scraper:
          self.switch_frame(self._2_inventory_scraper)
          self.scraper_assist_title.hide()
        else:
          self.scraper_assist_title.hide()
        
        # Notification
        if self.settings["config"]['scraper_alert'] is True:
          notification_messagebox_multi_gui(self.internal['tray_icon'], "Inventory Scraped", 'Autofarming has been resumed.' if self.settings["config"]['resume_after_scraping'] is True else "You need to resume autofarming manually.")
        
        # Essential for scraper
        self.change_currently_viewing_label(0)
        self.scraper_double_left_arrow.setEnabled(False)
        self.scraper_left_arrow.setEnabled(False)
        
        # Essential for scraper (2)
        if len(self.messenger.internal[self.account_id]['scraper_pages']) >= 2:
          self.scraper_right_arrow.setEnabled(True)
          self.scraper_double_right_arrow.setEnabled(True)
        if self.settings["config"]['resume_after_scraping'] is True:
          self.messenger.internal[self.account_id]['autofarming'] = True
        
        data = self.messenger.internal[self.account_id]['profile_data']

        # Essential for scraper (3)
        self.scraper_bot_level.setText(bot_level_html(data['level']))
        self.scraper_bot_balance.setText(bot_balance_html(data['wallet']))
        self.scraper_bot_bank.setText(bot_bank_html(data['bank']))
        self.scraper_bot_networth.setText(networth_html(data['net']))
        self.scraper_total_items.setText(total_items_html(data['total_items']))
        self.scraper_total_commands.setText(total_commands_html(data['total_commands']))
        self.scraper_unique_items.setText(unique_items_html(data['unique_items']))

        break
      
      update_account_settings(self.account_id, self.settings)

    def change_terminal_text(self, text : str, newline : bool = False):
      import time
      old_text = self.scraper_holder.text()
      if newline:
        self.scraper_holder.setText(f"""{old_text}
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">{time.strftime('[%H:%M:%S]')}</span> {text}<br /></p>""")  
      else:
        self.scraper_holder.setText(f"""{old_text}
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">{time.strftime('[%H:%M:%S]')}</span> {text}</p>""")

    def change_currently_viewing_label(self, update_value):
      if isinstance(update_value, str):
        if update_value == "max_left":
          self.messenger.internal[self.account_id]['scraper_current_page'] = 0
        if update_value == "max_right":
          self.messenger.internal[self.account_id]['scraper_current_page'] = self.messenger.internal[self.account_id]["scraper_max_pages"]-1
      elif isinstance(update_value, int):
        self.messenger.internal[self.account_id]['scraper_current_page'] += update_value
      self.scraper_currently_viewing.setText(alt_scraper_html_text(self.messenger.internal[self.account_id]["scraper_current_page"], self.messenger.internal[self.account_id]['scraper_max_pages']))

    def scraper_max_back(self):
      if self.messenger.internal[self.account_id]['scraper_pages'] is None:
        return
      self.scraper_inventory.setText(self.messenger.internal[self.account_id]['scraper_pages'][0])
      self.change_currently_viewing_label("max_left")
      self.scraper_double_left_arrow.setEnabled(False)
      self.scraper_left_arrow.setEnabled(False)
      self.scraper_double_right_arrow.setEnabled(True)
      self.scraper_right_arrow.setEnabled(True)
    
    def scraper_max_next(self):
      if self.messenger.internal[self.account_id]['scraper_pages'] is None:
        return
      self.scraper_inventory.setText(self.messenger.internal[self.account_id]['scraper_pages'][len(self.messenger.internal[self.account_id]['scraper_pages'])-1])
      self.change_currently_viewing_label("max_right")
      self.scraper_double_left_arrow.setEnabled(True)
      self.scraper_left_arrow.setEnabled(True)
      self.scraper_double_right_arrow.setEnabled(False)
      self.scraper_right_arrow.setEnabled(False)

    def scraper_next(self):
      if self.messenger.internal[self.account_id]['scraper_pages'] is None:
        return
      num = self.messenger.internal[self.account_id]['scraper_current_page']+1
      self.scraper_inventory.setText(self.messenger.internal[self.account_id]['scraper_pages'][num])
      self.change_currently_viewing_label(+1)
      if self.messenger.internal[self.account_id]['scraper_current_page']+1 == self.messenger.internal[self.account_id]["scraper_max_pages"]:
        self.scraper_double_right_arrow.setEnabled(False)
        self.scraper_right_arrow.setEnabled(False)
      self.scraper_double_left_arrow.setEnabled(True)
      self.scraper_left_arrow.setEnabled(True)

    def scraper_back(self):
      if self.messenger.internal[self.account_id]['scraper_pages'] is None:
        return
      num = self.messenger.internal[self.account_id]['scraper_current_page']-1
      self.scraper_inventory.setText(self.messenger.internal[self.account_id]['scraper_pages'][num])
      self.change_currently_viewing_label(-1)
      if self.messenger.internal[self.account_id]['scraper_current_page'] <= 0:
        self.scraper_double_left_arrow.setEnabled(False)
        self.scraper_left_arrow.setEnabled(False)
      self.scraper_double_right_arrow.setEnabled(True)
      self.scraper_right_arrow.setEnabled(True)

    def pre_select_items(self):
      # Search places      
      chosen_search_places = self.settings['config']['search_places']

      item : QtWidgets.QListWidgetItem
      for item in self.customization_main_search_list.findItems('*', QtCore.Qt.MatchWildcard):
        if item.text() in chosen_search_places:
          item.setSelected(True)

      # Crime actions
      chosen_crime_actions = self.settings['config']['crime_actions']
      
      item : QtWidgets.QListWidgetItem
      for item in self.customization_main_crime_list.findItems('*', QtCore.Qt.MatchWildcard):
        if item.text() in chosen_crime_actions:
          item.setSelected(True)

    def search_places(self, item):
      self.settings = get_account_settings(self.account_id)
      if item.text() in self.settings["config"]['search_places']:
        self.settings["config"]['search_places'].remove(item.text())
        return update_account_settings(self.account_id, self.settings)
      
      self.settings["config"]['search_places'].append(item.text())
      update_account_settings(self.account_id, self.settings)
    
    def crime_actions(self, item):
      self.settings = get_account_settings(self.account_id)
      if item.text() in self.settings["config"]['crime_actions']:
        self.settings["config"]['crime_actions'].remove(item.text())
        return update_account_settings(self.account_id, self.settings)        
      
      self.settings["config"]['crime_actions'].append(item.text())
      update_account_settings(self.account_id, self.settings)
      
    def essential(self):
      self.automation_polish_icon(self.automation_depositing, 'auto_dep')
      self.automation_polish_icon(self.automation_highlow, 'auto_highlow')
      self.automation_polish_icon(self.automation_begging, 'auto_beg')
      self.automation_polish_icon(self.automation_fishing, 'auto_fish')
      self.automation_polish_icon(self.automation_hunting, 'auto_hunt')
      self.automation_polish_icon(self.automation_digging, 'auto_dig')
      self.automation_polish_icon(self.automation_search, 'auto_search')
      self.automation_polish_icon(self.automation_trivia, 'auto_trivia')
      self.automation_polish_icon(self.automation_crime, 'auto_crime')
      self.automation_polish_icon(self.automation_meme, 'auto_meme')
      self.automation_polish_icon(self.automation_command_delay, 'command_delay')
      self.automation_polish_icon(self.automation_dm_mode, 'dm_mode')
      self.automation_polish_icon(self.automation_slots, 'slots')
      self.automation_polish_icon(self.automation_scratch, 'scratch')
      self.automation_polish_icon(self.automation_gamble, 'gamble')
      self.automation_polish_icon(self.automation_snakeeyes, 'snakeeyes')
      self.automation_polish_icon(self.automation_work, 'work')

      # These go within the automation because the settings are in the normal config
      self.automation_polish_icon(self.scraper_alert, "scraper_alert")
      self.automation_polish_icon(self.scraper_retry_success, "scraper_retry")
      self.automation_polish_icon(self.scraper_resume_autofarm, "resume_after_scraping")
      
      self.powerups_polish_icon(self.powerups_pizza, 'pizza')
      self.powerups_polish_icon(self.powerups_whiskey, 'whiskey')
      self.powerups_polish_icon(self.powerups_horseshoe, 'horseshoe')
      self.powerups_polish_icon(self.powerups_ammo, 'ammo')
      self.powerups_polish_icon(self.powerups_alcohol, 'alcohol')
      self.powerups_polish_icon(self.powerups_apple, 'apple')
      self.powerups_polish_icon(self.powerups_taco, 'taco')
      self.powerups_polish_icon(self.powerups_fishing_bait, 'fishingbait')
      self.powerups_polish_icon(self.powerups_cowboy_boots, 'boots')
      self.powerups_polish_icon(self.powerups_prestige_coin, 'prestige')
      self.powerups_polish_icon(self.powerups_robbers_mask, 'robbersmask')

      self.customization_polish_icon(self.customization_hooks_opt1, 'autofarm_logging')
      self.customization_polish_icon(self.customization_hooks_opt2, 'powerup_logging')
      self.customization_polish_icon(self.customization_hooks_opt3, 'event_sniping_logging')
      self.customization_polish_icon(self.customization_hooks_opt4, 'autotool_logging')
      self.customization_polish_icon(self.customization_hooks_opt5, 'autobuy_logging')
      self.customization_polish_icon(self.customization_hooks_opt6, 'levelup_logging')
      self.customization_polish_icon(self.customization_hooks_opt7, 'death_logging')
      self.customization_polish_icon(self.customization_hooks_opt8, 'work_logging')
      self.customization_polish_icon(self.customization_hooks_opt9, 'timestamps_logging')
      self.customization_polish_icon(self.customization_other_opt1, 'autobuypowerups')
      self.customization_polish_icon(self.customization_other_opt2, 'deathlifesaver')
      self.customization_polish_icon(self.customization_other_opt3, 'withdraw')
      self.customization_polish_icon(self.customization_other_opt4, 'embed_hooks')
      self.customization_polish_icon(self.customization_other_opt5, 'autotool')

      self.update_combo_on_startup(self.automation_premium_combo)
      self.update_combo_on_startup(self.automation_presence_combo)
      self.update_combo_on_startup(self.automation_job_combo)

      self.powerups_pizza_amount.setText(str(self.settings["powerups"]["pizza_amount"]))
      self.powerups_whiskey_amount.setText(str(self.settings["powerups"]["whiskey_amount"]))
      self.powerups_horseshoe_amount.setText(str(self.settings["powerups"]["horseshoe_amount"]))
      self.powerups_alcohol_amount.setText(str(self.settings["powerups"]["alcohol_amount"]))
      self.powerups_ammo_amount.setText(str(self.settings["powerups"]["ammo_amount"]))
      self.powerups_taco_amount.setText(str(self.settings["powerups"]["taco_amount"]))
      self.powerups_fishing_bait_amount.setText(str(self.settings["powerups"]["fishingbait_amount"]))
      self.powerups_apple_amount.setText(str(self.settings["powerups"]["apple_amount"]))
      self.powerups_prestige_coin_amount.setText(str(self.settings["powerups"]["prestige_amount"]))
      self.powerups_robbers_mask_amount.setText(str(self.settings["powerups"]["robbersmask_amount"]))
      self.powerups_cowboy_boots_amount.setText(str(self.settings["powerups"]["boots_amount"]))

      slots_bet = self.settings['config']['slots_bet'] if isinstance(self.settings['config']['slots_bet'], int) and self.settings['config']['slots_bet'] > 1 else 1
      self.automation_slots_input.setText(str(slots_bet))
      scratch_bet = self.settings['config']['scratch_bet'] if isinstance(self.settings['config']['scratch_bet'], int) and self.settings['config']['scratch_bet'] > 1500 else 1500
      self.automation_scratch_input.setText(str(scratch_bet))
      gamble_bet = self.settings['config']['gamble_bet'] if isinstance(self.settings['config']['gamble_bet'], int) and self.settings['config']['gamble_bet'] > 1500 else 1500
      self.automation_gamble_input.setText(str(gamble_bet))
      snakeeyes_bet = self.settings['config']['snakeeyes_bet'] if isinstance(self.settings['config']['snakeeyes_bet'], int) and self.settings['config']['snakeeyes_bet'] > 1500 else 1500
      self.automation_snakeeyes_input.setText(str(snakeeyes_bet))


    def update_combo_on_startup(self, item : QtWidgets.QComboBox):
      if item == self.automation_job_combo:
        _jobs = ["Automatic", "Discord Mod", "Babysitter", "Fast Food Cook", "House Wife", "Twitch Streamer", "YouTuber", "Professional Hunter", "Professional Fisherman", "Bartender", "Robber", "Police Officer", "Teacher", "Musician", "Pro Gamer", "Manager", "Developer", "Day Trader", "Santa Claus", "Politician", "Veterinarian", "Pharmacist", "Dank Memer Shopkeeper", "Lawyer", "Doctor", "Scientist", "Ghost"]
        valid = self.settings['config']['preferred_job'] if self.settings['config']['preferred_job'] in _jobs else "Automatic"
        item.setCurrentText(valid)
        return

      options_list = [
        
        ["Donor" , True , 'premium_status', self.automation_premium_combo],
        ["Normie", False, 'premium_status', self.automation_premium_combo],
        
        ["Online",               "online",    'account_presence', self.automation_presence_combo],
        ["DND (Do Not Disturb)", "dnd",       'account_presence', self.automation_presence_combo],
        ["Idle",                 "idle",      'account_presence', self.automation_presence_combo],
        ["Invisible",            "invisible", 'account_presence', self.automation_presence_combo],
        
      ]
      for list_ in options_list:
        if item == list_[3]:
          if list_[1] == self.settings["config"][list_[2]]:
            item.setCurrentText(list_[0])
            break

    def set_combo_values(self, item : QtWidgets.QComboBox):
      self.settings = get_account_settings(self.account_id)
      if item == self.automation_job_combo:
        self.settings['config']['preferred_job'] = item.currentText()
        update_account_settings(self.account_id, self.settings)
        return
      
      options_list = [
        
        ["Donor" , True , 'premium_status', self.automation_premium_combo],
        ["Normie", False, 'premium_status', self.automation_premium_combo],
        
        ["Online",               "online",    'account_presence', self.automation_presence_combo],
        ["DND (Do Not Disturb)", "dnd",       'account_presence', self.automation_presence_combo],
        ["Idle",                 "idle",      'account_presence', self.automation_presence_combo],
        ["Invisible",            "invisible", 'account_presence', self.automation_presence_combo],
        
      ]
      for list_ in options_list:
        if item == list_[3]:
          if list_[0].lower() == list_[3].currentText().lower():
            self.settings["config"][list_[2]] = list_[1]
            break
          
      update_account_settings(self.account_id, self.settings)

    def customization_change_icon(self, button : QtWidgets.QPushButton, state : str):
      self.settings = get_account_settings(self.account_id)
      self.settings["customization"][state] = not self.settings["customization"][state]
      image = switch_on_b64 if self.settings["customization"][state] is True else switch_off_b64
      button.setIcon(iconFromBase64(image))
      update_account_settings(self.account_id, self.settings)

    def powerups_change_icon(self, button : QtWidgets.QPushButton, state : str):
      self.settings = get_account_settings(self.account_id)
      self.settings["powerups"][state] = not self.settings["powerups"][state]
      image = switch_on_b64 if self.settings["powerups"][state] is True else switch_off_b64
      button.setIcon(iconFromBase64(image))
      update_account_settings(self.account_id, self.settings)

    def automation_change_icon(self, button : QtWidgets.QPushButton, state : str):
      self.settings = get_account_settings(self.account_id)
      self.settings["config"][state] = not self.settings["config"][state]
      image = switch_on_b64 if self.settings["config"][state] is True else switch_off_b64
      button.setIcon(iconFromBase64(image))
      update_account_settings(self.account_id, self.settings)

    def automation_polish_icon(self, button : QtWidgets.QPushButton, state : str):
      """ Used on startup. Useful to make settings look enabled if they were enabled, and vice versa. """
      
      image = switch_on_b64 if self.settings["config"][state] is True else switch_off_b64
      button.setIcon(iconFromBase64(image))

    def powerups_polish_icon(self, button : QtWidgets.QPushButton, state : str):
      """ Used on startup. Useful to make settings look enabled if they were enabled, and vice versa. """
      
      image = switch_on_b64 if self.settings["powerups"][state] is True else switch_off_b64
      button.setIcon(iconFromBase64(image))

    def customization_polish_icon(self, button : QtWidgets.QPushButton, state : str):
      """ Used on startup. Useful to make settings look enabled if they were enabled, and vice versa. """
      
      image = switch_on_b64 if self.settings["customization"][state] is True else switch_off_b64
      button.setIcon(iconFromBase64(image))
      
    def switch_frame(self, item):
      # Internal data setting
      self.internal['current_frame'] = item
      item.raise_()

      # Important for scraper
      if item == self._2_inventory_scraper:
        if self.messenger.internal[self.account_id]['scraper_working'] is True:
          self._0_scraper_assist.raise_()
          self.scraper_assist_title.show()
        else:
          self.scraper_assist_title.hide()

    def retranslateUi(self, MainWindow):
      _translate = QtCore.QCoreApplication.translate
      MainWindow.setWindowTitle(_translate("MainWindow", "Darkend - Dank Memer Autofarm By Sxvxge"))
      self.automation_depositing.setText(_translate("MainWindow", "Auto Depositing"))
      self.automation_fishing.setText(_translate("MainWindow", "Auto Fishing"))
      self.automation_hunting.setText(_translate("MainWindow", "Auto Hunting"))
      self.automation_digging.setText(_translate("MainWindow", "Auto Digging"))
      self.automation_title.setText(_translate("MainWindow", "<center>Darkend - Automation Menu</center>"))
      self.automation_highlow.setText(_translate("MainWindow", "Auto High-Low"))
      self.automation_begging.setText(_translate("MainWindow", "Auto Begging"))
      self.automation_premium_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:15px; font-weight:600;\">Account Premium State</span></p></body></html>"))
      self.automation_presence_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:15px; font-weight:600;\">Account Presence</span></p></body></html>"))
      self.automation_meme.setText(_translate("MainWindow", "Auto Post Meme"))
      self.automation_search.setText(_translate("MainWindow", "Auto Search"))
      self.automation_crime.setText(_translate("MainWindow", "Auto Crime"))
      self.automation_trivia.setText(_translate("MainWindow", "Auto Trivia"))
      self.automation_go_back.setText(_translate("MainWindow", "Go Back"))
      self.automation_command_delay.setText(_translate("MainWindow", "Command Delay"))
      self.automation_dm_mode.setText(_translate("MainWindow", "DM autofarm mode"))
      self.automation_snakeeyes.setText(_translate("MainWindow", "Auto Snake-Eyes"))
      self.automation_work.setText(_translate("MainWindow", "Auto Work"))
      self.automation_gamble.setText(_translate("MainWindow", "Auto Gamble"))
      self.automation_scratch.setText(_translate("MainWindow", "Auto Scratch"))
      self.automation_slots.setText(_translate("MainWindow", "Auto Slots"))
      self.automation_slots_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:15px; font-weight:600;\">Slots bet</span></p></body></html>"))
      self.automation_scratch_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:15px; font-weight:600;\">Scratch bet</span></p></body></html>"))
      self.automation_gamble_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:15px; font-weight:600;\">Gamble bet</span></p></body></html>"))
      self.automation_snakeeyes_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:15px; font-weight:600;\">Snakeeyes bet</span></p></body></html>"))
      self.automation_scratch_input.setText(_translate("MainWindow", "1500"))
      self.automation_slots_input.setText(_translate("MainWindow", "1"))
      self.automation_gamble_input.setText(_translate("MainWindow", "1500"))
      self.automation_snakeeyes_input.setText(_translate("MainWindow", "1500"))
      self.scraper_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Darkend - Inventory Scraper</p></body></html>"))
      self.scraper_inventory.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The inventory hasn\'t been cached yet.</p></body></html>"))
      self.scraper_holder.setText(_translate("MainWindow", "<html><head/><body><p>Darkend Terminal [Version 0.3]<br/>The First GUI-based Dank Memer Autofarm.<br/></body></html>"))
      self.scraper_refresh_button.setText(_translate("MainWindow", "Scrape Inventory"))
      self.scraper_resume_autofarm.setText(_translate("MainWindow", "Resume Autofarming after scraping"))
      self.scraper_retry_success.setText(_translate("MainWindow", "Keep retrying until success"))
      self.scraper_alert.setText(_translate("MainWindow", "Alert on refresh"))
      self.scraper_currently_viewing.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Currently Viewing: N/A</span></p></body></html>"))
      self.scraper_go_back.setText(_translate("MainWindow", "Go Back"))
      
      self.scraper_bot_balance.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:15px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bot Balance: N/A</span></p></body></html>"))
      self.scraper_bot_bank.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:15px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bot Bank: N/A</span></p></body></html>"))
      self.scraper_bot_level.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:15px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bot Level: N/A</span></p></body></html>"))
      self.scraper_bot_networth.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Bot Networth: N/A</span></p></body></html>"))
      self.scraper_unique_items.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Unique Items: N/A</span></p></body></html>"))
      self.scraper_total_items.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Total Items: N/A</span></p></body></html>"))
      self.scraper_total_commands.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:13px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15px; font-weight:600;\">Total Commands: N/A</span></p></body></html>"))
      
      self.powerups_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Darkend - Powerups</p></body></html>"))
      self.powerups_ammo.setText(_translate("MainWindow", "Auto Ammo"))
      self.powerups_alcohol.setText(_translate("MainWindow", "Auto Alcohol"))
      self.powerups_pizza.setText(_translate("MainWindow", "Auto Pizza"))
      self.powerups_apple.setText(_translate("MainWindow", "Auto Apple"))
      self.powerups_reset_button.setText(_translate("MainWindow", "Reset Quantities"))
      self.powerups_go_back.setText(_translate("MainWindow", "Go Back"))
      self.powerups_prestige_coin.setText(_translate("MainWindow", "Auto Presetige Coin"))
      self.powerups_fishing_bait.setText(_translate("MainWindow", "Auto Fishing Bait"))
      self.powerups_robbers_mask.setText(_translate("MainWindow", "Auto Robbers Mask"))
      self.powerups_alcohol_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_taco.setText(_translate("MainWindow", "Auto Taco"))
      self.powerups_whiskey.setText(_translate("MainWindow", "Auto Whiskey"))
      self.powerups_horseshoe.setText(_translate("MainWindow", "Auto Horseshoe"))
      self.powerups_cowboy_boots.setText(_translate("MainWindow", "Auto Cowboy Boots"))
      self.powerups_pizza_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_apple_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_ammo_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_robbers_mask_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_fishing_bait_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_prestige_coin_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_cowboy_boots_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_taco_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_horseshoe_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.powerups_whiskey_amount.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">This is the amount of the powerup you\'d like to automatically use whenever the cooldown is over.<br/>If enabled and set to 0, the bot will automatically purchase the powerup if the setting was enabled at the Customization section and the powerup is enabled</p></body></html>"))
      self.switcher_automation_view.setText(_translate("MainWindow", "View"))
      self.switcher_scraper_view.setText(_translate("MainWindow", "View"))
      self.switcher_autopowerups_view.setText(_translate("MainWindow", "View"))
      self.switcher_customization_view.setText(_translate("MainWindow", "View"))
      self.switcher_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Darkend - Switcher</p></body></html>"))
      self.switcher_automation_info.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Automation<br/></span><span style=\" font-size:13px;\">Automate economy commands<br/>with ease</span></p></body></html>"))
      self.switcher_scraper_info.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Inventory Scraper<br/></span><span style=\" font-size:13px;\">The most advanced inventory<br/>scraper, with many useful features.</span></p></body></html>"))
      self.switcher_autopowerups_info.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Auto-Powerups<br/></span><span style=\" font-size:13px;\">Automatically use powerups to<br/>maximize the coins and EXP</span></p></body></html>"))
      self.switcher_customization_info.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Customization<br/></span><span style=\" font-size:13px;\">Customize how Darkend works<br/>to fit your own standards</span></p></body></html>"))
      self.switcher_ultimate_view.setText(_translate("MainWindow", "View"))
      self.switcher_ultimate_info.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Coming soon<br/></span><span style=\" font-size:13px;\">Stay tuned for Darkend\'s<br/>next game-changing features!</span></p></body></html>"))
      self.switcher_coming_soon_info.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Coming soon<br/></span><span style=\" font-size:13px;\">Stay tuned for Darkend\'s<br/>next game-changing features!</span></p></body></html>"))
      self.switcher_coming_soon_view.setText(_translate("MainWindow", "View"))
      self.customization_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Darkend - Customization</p></body></html>"))
      self.customization_hooks.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Webhooks</span></p></body></html>"))
      self.customization_other_opt3.setText(_translate("MainWindow", "Auto Withdraw"))
      self.customization_other_opt2.setText(_translate("MainWindow", "LifeSaver on Death"))
      self.customization_other.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Other</span></p></body></html>"))
      __sortingEnabled = self.customization_main_search_list.isSortingEnabled()
      self.customization_main_search_list.setSortingEnabled(False)
      self.customization_main_search_list.setSortingEnabled(__sortingEnabled)
      self.customization_main_search.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Search Places</span></p></body></html>"))
      self.customization_main_crime.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:27px;\">Crime actions</span></p></body></html>"))
      __sortingEnabled = self.customization_main_crime_list.isSortingEnabled()
      self.customization_main_crime_list.setSortingEnabled(False)
      
      crime_actions = ['bank robbing', 'murder', 'identity theft', 'trespassing', 'hacking', 'Eating a hot dog sideways', 'dui', 'arson', 'piracy', 'fraud', 'tax evasion', 'drug distribution', 'treason', 'vandalism', 'littering', 'boredom', 'cyber bullying', 'shoplifting']
      for index, action in enumerate(crime_actions):
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.customization_main_crime_list.addItem(item)
        item.setText(_translate("MainWindow", action))

      search_places = ["ZomB's Grave", 'twitter', 'fridge', "soul's chamber", 'pocket', "aeradella's home", 'dumpster', 'washer', 'dog', 'shoe', 'vacuum', 'dresser', 'bushes', 'crawlspace', 'ocean', 'dark room', 'police officer', 'attic', 'lego bin', 'glovebox', 'couch', 'toilet', 'pantry', 'Supreme Court', 'sewer', 'bank', 'street', 'basement', 'book', 'kitchen', 'hospital', "mcdonald's", 'who asked', 'purse', 'twitch', "god's own place", 'toxic waste plant', 'tesla', 'beehive', 'sink', 'movie theater', 'Immortals Dimension', 'car', 'coat', 'mailbox', 'air', 'phoenix pits', 'briefcase', 'tree', 'uber', 'bus', 'bathroom', 'computer', 'bed', 'van', 'grass', 'garage']
      for index, place in enumerate(search_places):
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.customization_main_search_list.addItem(item)
        item.setText(_translate("MainWindow", place))

      self.customization_main_crime_list.setSortingEnabled(__sortingEnabled)
      self.customization_go_back.setText(_translate("MainWindow", "Go Back"))
      self.customization_other_opt4.setText(_translate("MainWindow", "Embed Logs"))
      self.customization_other_opt1.setText(_translate("MainWindow", "Auto Buy Powerups"))
      self.customization_other_opt5.setText(_translate("MainWindow", "Auto Tool"))
      self.coming_soon_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Coming Soon!</p></body></html>"))
      self.scraper_assist_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Scraping Inventory...</p></body></html>"))
      self.automation_job_label.setText(_translate("MainWindow", '<html><head/><body><p align="center"><span style=" font-size:15px; font-weight:600;">Job</span></p></body></html>'))

      self.customization_hooks_opt1.setText(_translate("MainWindow", "Autofarming state logging"))
      self.customization_hooks_opt2.setText(_translate("MainWindow", "Auto Powerup logging"))
      self.customization_hooks_opt3.setText(_translate("MainWindow", "Event Sniping logging"))
      self.customization_hooks_opt4.setText(_translate("MainWindow", "Auto Tool logging"))
      self.customization_hooks_opt5.setText(_translate("MainWindow", "Auto Buy logging"))
      self.customization_hooks_opt6.setText(_translate("MainWindow", "Level up logging"))
      self.customization_hooks_opt7.setText(_translate("MainWindow", "Death logging"))
      self.customization_hooks_opt8.setText(_translate("MainWindow", "Work logging"))
      self.customization_hooks_opt9.setText(_translate("MainWindow", "Include timestamps"))

if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  MainWindow = QtWidgets.QMainWindow()
  ui = AltGUI()
  ui.setupUi(MainWindow)
  MainWindow.show()
  sys.exit(app.exec_())
