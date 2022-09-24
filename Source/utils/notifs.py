import os

# Paths
appdata = os.getenv('APPDATA')
directory = f"{appdata}\\Darkend v1"
logo = f'{directory}\\logo.png'
logo_b64 = b'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'

def iconFromBase64(base64):
  from PyQt5 import QtGui, QtCore
  pixmap = QtGui.QPixmap()
  pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
  icon = QtGui.QIcon(pixmap)
  return icon

def show_critical_messagebox(title, text):
  from PyQt5.QtWidgets import QMessageBox
  from PyQt5.QtCore import Qt
  msg = QMessageBox()
  msg.setWindowIcon(iconFromBase64(logo_b64))
  msg.setIcon(QMessageBox.Critical)
  msg.setText(text)
  msg.setWindowTitle(title)
  msg.setStandardButtons(QMessageBox.Ok)
  
  retval = msg.exec_() #msg.exec_()
  print(retval)
  return retval

def show_info_messagebox(title, text):
  from PyQt5.QtWidgets import QMessageBox
  msg = QMessageBox()
  msg.setWindowIcon(iconFromBase64(logo_b64))
  msg.setIcon(QMessageBox.Information)
  msg.setText(text)
  msg.setWindowTitle(title)
  msg.setStandardButtons(QMessageBox.Ok)
  retval = msg.exec_()
  return retval
  
def show_info_messagebox_cancel(title, text):
  from PyQt5.QtWidgets import QMessageBox
  msg = QMessageBox()
  msg.setWindowIcon(iconFromBase64(logo_b64))
  msg.setIcon(QMessageBox.Information)
  msg.setText(text)
  msg.setWindowTitle(title)
  msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
  retval = msg.exec_()
  return retval

def notification_messagebox(tray, title, text):
  try:
    tray.showMessage(title, text, iconFromBase64(logo_b64), 5000)
    return 1
  except:
    code = show_info_messagebox(title, text)
    return code

def notification_messagebox_multi(tray, title, text):
  try:
    tray.showMessage(title, text, iconFromBase64(logo_b64), 5000)
    return 1
  except:
    code = show_info_messagebox(title, text)
    return code

def critical_messagebox_multi(tray, title, text):
  try:
    tray.showMessage(title, text, iconFromBase64(logo_b64), 5000)
    return 1
  except:
    code = show_critical_messagebox(title, text)
    return code

def critical_messagebox_multi_gui(tray, title, text):
  try:
    tray.showMessage(title, text, iconFromBase64(logo_b64), 5000)
    return 1
  except:
    code = show_critical_messagebox(title, text)
    return code

def notification_messagebox_multi_gui(tray, title, text):
  try:
    tray.showMessage(title, text, iconFromBase64(logo_b64), 5000)
    return 1
  except:
    code = show_critical_messagebox(title, text)
    return code

def critical_messagebox(tray, title, text):
  try:
    tray.showMessage(title, text, iconFromBase64(logo_b64), 5000)
    return 1
  except:
    code = show_critical_messagebox(title, text)
    return code