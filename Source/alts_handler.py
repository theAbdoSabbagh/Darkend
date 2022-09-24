from PyQt5 import QtCore, QtGui, QtWidgets
from qasync import asyncSlot
from utils.alt_handler_assist import create_account_file, get_account_settings, update_account_settings, ensure_new_keys_get_added, view_account_logs

edit_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAaRJREFUaEPtmP9NwzAQhd/bgA0YAdgANoAJgA3oJnQC2AA2oBvQjsAGbGBkKakiE/tsxz8uUvKv1fT7/M5n5YiVP1w5PzaB3gluCZRMwBhzAeARwDWAI8m99H41CQzwXwP8yH0EcEfy1yeiQsADHyWhReAewEegXGw53cytqxCwYMaYJwBvAYkdyVd3vZvAUDa3JD9HKEFiT/JFhYBT888k3yMkdCTgObCSxImkba3/nqYlJHQbn8QJgC212VbaTMAD/wPgcrKtroTtTofu94CvbADYA3wAcOWT6H4TSzU/rNsbd5rEw7Q7hSSqlpAE7+n/wZpv1kZbwFuZKgm0gq8i0BK+uEBr+KICPeCLCfSCLyLQE36xQG/4RQIa4LMFtMBnCWiCTxbQBp8koBE+WkArfJSAZnhRQDt8UGAN8JLAtzNoFUcfoemB9G2bu+79oDHGmMC0wB0DJn0G5sImzYWmAiTPojPjv27wUgmdExgFtMFHC3gi77rzI1PsGXAdVMDnJqAGXrzISnaLWu+qMheqBZvURltCLPmvLYElu1fit6tP4A+XnGFADD6wIAAAAABJRU5ErkJggg=='
trash_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAWdJREFUaEPtWdtRwzAQ3K0AOqAE6ADohBJCBZAOKCGdAB2EDqADqGCZm5EZkzg6WbHGONzN+Md63d5KK51ELNy4cP8RAOZmMBg4CQYkPQJ4GAlmTdLaHWXuFJJU4tgNAPvG2AsA+7JGcp2rUAJA3iAty0lmffwXALp52p9KWVqPYGRvDG+duAx0zkj6mUoerbUAasYIALXRHmo3KwOSrgCcJcfeSH72nZR0DuAy/fsiud0FMTcA0/Tr5NQtyV8aL8n2iedU/kpyb98IALn57EVHUjDgBWkowJPJaDAAIBiIRRz7wPgDY6hQ77gdG1nIaMhoyGjI6OFV4CnEKZxGnwBYXmy22s15U85sdcy2JFd/Kiee4nbCY7lpQhMA5k5olsDAO4CLKRwt6MMuxjpByFYfc5yueYUp8HWwyj3JTrGmAWC9pKeku4ZMfADYeFfqfUTFDNSGsnW7ANA6wl7/wYAXodbli2fgG9OS20DPyMUYAAAAAElFTkSuQmCC'
settings_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAABGJJREFUaEPtmf2VDUEQxetGgAgQASJABFYEiMCKABEgAkSACKwIrAgQgd0Iyvntqd5Tr6d7et4zPp6z/c+enZmurlsft6rryfZ8ac/1twsAf9uDq3rA3d+b2b0BqA+SDtYCvjaAz2Z2c6DcsaRb/yoAX6KYpNUMt5ogd8fyeID1SdKdDMbdj8zsdjy7Jel4CdjRN2sCQOGPceBbSQ8rAG/M7EE8uysJQL+8hgDc/bKkk9FJ7v7MzJ7Gd88l8f/5Gr1vyV9y9hIAWPWymb2U9LZzENZ/kRL4kSQsngHgkdfxgPCZk4enDs3sRNLdOePNAnB36O5dEvCNg82MEDmJuEfxjXg3s0mIuHsOsSISIE8IJ6wdIYbi19KZ9yVBz801AvC1ElaEEFII3YjzePnFzA4kATZ7AKXwSknk/JrnGAsQ9fom6frWAKqYPTUzFLrREcR7PENYzOZLWBrg5MiljjyMAODyfpJTZV/TA3EI1i8WORMQYYCLc7VtWnwubnkXZ+DF7JEPYQRCKpMCRrneMk4PANZ8HEp8JznzZnfHOgAxSWd/d13uzlksvHcedgGQ/4sXXrXOmgAI5bB+WRNG2VXZbfe5e2YutuOFjdxqAYA2M6scSnq1w+GERumL6H8+7SCDKCgeYvtRTastAKBmU04wYhVPLClosAl8XzMKe5HRpcQCMMIHGblrhSge1vt7OUCMc1BmHVyHAt0WwN05tEWt2fhvJD3qeSOIgtqTDYD3UH4jfM5ycM6tkWAlmcunFJ7s1rPnjaJH8hdrY8mr6axmcXJ3CIHCmFeXQocAkmIUmllOdvcfyWqjZo4W4UptvIo6MQAFcbZrHfZCASK3whPrVW3Cd0m5FTjX090JgeKJVruRW5dJS96Kll0AtA7Orm/ydRgi15dJKFaGuACQXb9NCHWbL3fPzeGfCaFgl8zrTVZwd3i+JPqEKiuKPZU06Twb/Q/5NntzG9EolFb3OktplITNNDrs8Ts0+kzS8x7dzxUyikkekUBrFJO5Qpbvvb0zJxSbP4xERk6uG1Ap3hgXsmigsHx2MW0uyi9tJXLdKPo1W4EWymglkJHbds7G+xtX1VYvlBMW+c2QGTVmYcnczG09hWiE1IRa/792ulFwJrehuDPQIxFmeGgYWjOhQriynwJYX2jyrXDZhSYAoFi+DeUrJYrnNpcEo0vdatIWEw3oORMFrIWi9ZWS/Lm2+EoZIOo7KYDmBrckF0AnTFGxDHTKAGyu7cYYfFeIpJuHozqQm6+sBxbBWmVUmN81KS/Crqbmso+BGV5tTSm6zeGwne70+DRkVNoy2OL/etazdLDFRAN6Pk7jFgrn8O5QkA+70Zgql9HiBgcXIQGUkCs3uFbLnS/oKM4UoiePb8tosZ76bfDBEgD7PdwdFazKC2WOOqE8d/874/UtAOz3DxxBvfv7E1MAgEJ7A+DizC+SRj8ELnX8uj907/3PrIvNtuKHQxpd8azfIuoCwG8x6xZCfwIVVWVPRSt+QQAAAABJRU5ErkJggg=='
discord_icon_b64 = b'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'
logo_b64 = b'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'
globalize_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAA9JJREFUaEPtmY9RVDEQxverQK1AqECpQKlArUCoQKlAqECoQKhArMCjAo8KpAO1gnW+mw2z9y4v2Ze8O2WGzNww3OUl+9v/yYM88IEHLr88AvxrC85mAVXdE5E3IvJaRJ7a56UBLkXkt30WIvINwN0c8F0AqkpBP5nQSdioXIQizBkAwjWNJgAT/IOIfDRNN21uD1H4cxG5aAGZDKCqb0XkywyCD6EJcgzgeoo2JgGoKt3ldMoGhbnHInIkIq8Gc04BnEX3CAGYy1Dr1P5c4xDAwixKF3ruFqYVaI1qbEQBvs4s/B8R2UsCmoIYT7RwGpcAaKXiqAKoKl3GL1xbM/I7M8+GK2b2ys7zGxQBzLzU/pyjKJSqXorIe7fhu1JgjwKYWX82ZptbS7Fr4PT5iCYGEIyD/bF4KAH0uM4NAFbkpmHKY6FLgT1qtSxAp/YpdBcAF1BVplhmPo5RK4wBMK2x0raObgCDYL+UrMBKzUy17pY5CVWVvs/mrHXMBeCtsARwUAWwrpIAPSOrrZYFVZXu88SeZTCvdbEbLqSqNNPn4GY31lH66XcAmApnGarKqsw2neMEAN37fuQA/AMX1q8kDQyFqhaaXopBceM5Yq2dyQEwV6cGK/kcv8tB7ALAx8FGbOUAfojI6nACYPW7qvL/HMQuAFhPvpslNwI5B6DJ7AmgALELAJ76fuVkWil56KOqmgWoWGKqq58DOIk+VJIpB8AS/mIsbRXcKSpPmncAgHtVhwO4BbB29q4F8erQkbHSWExUhXETsmtn9vIxEApin0Z5Ksrm9BksEQXwWSiURn0huwLABbKjEyIK4PuyUCFjD5RaCVbV/ZJfdEBEAXxfVm8lLNv4QK5u1Hhyi6zr/X8jgLNp1AC82RYADitW8BtFAzkCwAKWDkaT2mkWD3Z9qX0obqaqLQBMDqmzpMWZYe6vUQZrrt1ieA1Fj5TcgBDZe5qZWnCuzT2WdiKk9lPOn3akNDcaWqF4T6OqvgmMutFw3uroaO18yn6j2h+NgbRqJjhLdYHZi5Yaa72jUFSEvxBou1ZxEMPbiRIErcb5FCC1I1HBc/OqzWL1Zs7cyVdnflW8gG0M6iFAsYimyVEAapZZIx3t+DzdhdbYaMhmALjixdhsl7sFd+JPBGOOvgfpBKi6TSiNFvofnkkp9DBYCUBX499n7lIqGgPMNkdbfcHhLEGXYtPHT2/WoeCs/DzkVN8HDLURioGCNXqyDi+AmTKZECYLPimIIz5g1Zju5V+zplRKYf1r1uv/4jVrBGzbc7pcaNvCRdZ/BIhoaZtz/gLCfsZAH32QHgAAAABJRU5ErkJggg=='
view_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAA9ZJREFUaEPtmI9RlDEQxXcr0A7ECsQKhArUCpQKxAqECtQKhA6gAqECpQK1A61gnR+ze7OXS77kO7hRZr7MMHPc5c++3ZeXl6g88KYPPH5ZAPzrCi4VWCpwxwwsFCKBZvZYRF6IyL6IHHhS+cz3tN8i8t0/X/nna1Xl+zu1O1XAzN6IyNsU9NxgAHOmqudzB0b/rQCY2QcROU4Z3nb9GEclPqnq6dyJZgEwM+jxRUT2Kgtdi0jQ45YyQRGnWFAqaAblyvZTRI5UlXmG2jAAMyNw6JLbLzLnNJjFZzMjCa+8kk+KeaHV0QiCLgDP3lffoDEngZ+o6tnIIr0+ZkZiTkQkA2HTH/Y2+iQAM6PcBB9qQixsuOPexGYWqsQY6ATFms0TRTURhrw3ABEKtjG+CcBL/K0IHn42s+5joFpIabkg3GYOuF5tZoY4fCxAPG0lrAqgQps/8F9VLyYWfuc0yNWqdWevQL/PE3NBKarxyPs06dQCAG0iiwR/MFXGStYYE4pEDKE8ERDfvVdVgmxVgjHMEWOuVPWw7LwBoAiGQPY7JUdNMtUuvVprquRVhX4vPQh+f96ZGxDMHW0D9BoA37STA8oMmFmu1qWqIo1TmxUaBohqVvNgM0OdODijAXq1qUsAORi8SmszrmYzM/N/qNbegDqxR9jEt9RQ1REpJ+Bnvs4a6NVgP2UBQOtSh07FmG72A7WZ5Sogk5Mnb4UZqzEZQM7+5AZLgWTJO1VVyt1tBS1G18pUWlUhAyAL4U9GJ/1XAFb0blGoqxD/HYU8oFyFrkL4mNjEgG6emIl2bOIfccIPbmKUEUmlrYnLfchoBn2hqq87MjpL6WbJqGc087pLJfc/yFycmCgMfqd2kOGT4pzoKt3IudSyEjmrBDLpCBsGrGYlsk/qGcPSCVfPpSkzRwBxeACCBafMHJVD6rLfqbGJzGPHp1wtZg5HGoBv3I9tXJp6djpTg2BYeMpF4osIrHZdvN2A7pOm7DSuNpu8yRN+5EKTHSFBECDnxOQV0k/pUA4uNL3TlmyT9Xxt7TrhER/CxJlOgCCDePqtn0Myt/x5Bvrlx4ImbfLYLoCk32Q+X/cCCOXGBzVpUdsIrl64UvZO+cpxrqrlA0JVnYcBpJMXIOUrAj9TpfysclM8qyAIVDMuNzWny2MBN7/7f1YpSk65yVxPcbrGzjvAdR62hszgVhRq0IAy89dSnR4AVIk3oK2fZ2ZRqBWNXxehRPm4GxUiw+XjLl5r1mNYbf17AdBL8y5/XwDsMrsjcy8VGMnSLvssFdhldkfmXiowkqVd9nnwFfgL+7jWQDlOPvAAAAAASUVORK5CYII='
pause_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAKlJREFUaEPtl0sOgCAMRDsn06PryUrcKYk0hBRDfG6LfGba8pAt/mnx/RsH+NpBHMCBQQVIoUEBh3//nwPu7g3ZTkl7S1Z3P8xsexsjqUvUrsHXohwAB57JRwpVxUgR04Wiq5E2ShuljcJCwNy9CkAJUKJSAJQAJXgT86hvVwE4DU6D04vjdHTRzY530+jsDUbrcYBIoew4DmQrHM2PA5FC2XEcyFY4mr8AAeb8MQE+guQAAAAASUVORK5CYII='
close_icon_b64 = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAUlJREFUaEPtmNEOgyAMRemXbn7Z3JeykGjCQ8W29yIhw9fNck4vq0xJk18yOX9aAqMTXAmsBMAOrC0ENhC+/f8SyDm/RWSHW6cUiNR2JZBzLuCvlNIuIhtTIlrbLFC6k1L6VNA0iQr+LL9ZUzYLlMrKQrCEUvMrIqVZpsslwJZA4QuPW4AlwYAPC6ASLHhIICrBhIcFvBJseIqAVaIHPE3gTqIXPFXgSuKYdOXpfV6uOX/3MAiN0VZRpdv116nw9ARO0gsJOvzTAvCxQ0v+6S1El6AKaNPm6Fr9I6ZK0ARao7LHKfbcThQBy5zvJQELWOAb0wneTpCAB76XRFggAt9DIiSAwLMl3AIMeKaES4AJz5IwCyivVWhnmxGvVWjwShKu2uYEqoXmfbV49+dixOfuBEZAttZcAqMTWQmsBMAOrC0ENhC+ffoEfn4d+DFO/D3mAAAAAElFTkSuQmCC'

def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

def new_username_text(username):
  return f'<p align="left" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:13px; font-weight:600;">{username}</span></p>'

def new_add_account_title_text(text):
  return f'<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">{text}</span></p></body></html>'

class messenger():
  # Doesn't have pre-set data because it's set in the bot function automatically.
  # This is so each account doesn't interfere with the other
  internal = {}

class shadow():
  internal = {
    "config" : {
      'close_now' :          False,
      'current_frame' :       None,
      'autofarming' :         None,
      'channel_id' :          None,
      'waiting_presence':     None,
      'tray_icon': None,
      'search_places': [],
      'crime_actions': [],
      'to_buy': [], # tools
      'powerups_to_buy': [], # powerups
      'other_to_buy': [], # other
      "autobuying_busy": False,
      "active_items": {},
      "start_scraping": False,
      "scraper_pages": None,
      "scraper_working": False,
      "scraper_current_page": 0,
      "scraper_max_pages": 0,
      "scraper_last_page_item_amount": 0,
      "last_height": None,
      "account_widgets": [],
      "widget_values": {},
      "previous_token": "",
      "previous_channel_id": "",
      "previous_account_username": "",
      "previous_father": "",
      "previous_webhook_url": "",
      'accounts_added_at_startup': 0,
      "bots_running": None,
    },

    "versions" : {
      'isPublic' : False,
      'isPrivate': True,
      'public_version': '0.65',
      'private_version': '0.65',
    }
  }

class Ui_MultipleAccounts(object):
    def setupUi(self, MultipleAccounts):
      MultipleAccounts.setObjectName("MultipleAccounts")
      MultipleAccounts.resize(838, 451)
      MultipleAccounts.setStyleSheet("""
QScrollBar:vertical {
	color: white;
  background-color: white;
  width: 12px;
  margin: 15px 0 15px 0;
	border-radius: 0px;
}
QScrollBar::handle:vertical {
	background-color: transparent;
	min-height: 50px;
	border-radius: 6px;
	border: 2px solid rgb(39,65,100);
}
QScrollBar::handle:vertical:hover{
 background-color: rgb(39,65,100);
}
QScrollBar::sub-line:vertical {
	border: none;
	background-color:none;
}
QScrollBar::add-line:vertical {
	border: none;
	background-color:none;
}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
	background-color: rgb(20, 28, 36);
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	background-color: rgb(20, 28, 36);
}
QToolTip {
	background-color: rgb(27, 27, 27);
	color: white;
	text-align: cetner;
	border: 2px solid black;
	font-family: Century Gothic;
}""")
      self.centralwidget = QtWidgets.QWidget(MultipleAccounts)
      self.centralwidget.setObjectName("centralwidget")

      self.global_frame = QtWidgets.QFrame(self.centralwidget)
      self.global_frame.setGeometry(QtCore.QRect(0, 0, 841, 451))
      self.global_frame.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
      self.global_frame.setStyleSheet("background-color: rgb(20, 28, 36);")
      self.global_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.global_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self.global_frame.setObjectName("global_frame")
      self.verticalLayout = QtWidgets.QVBoxLayout(self.global_frame)
      self.verticalLayout.setObjectName("verticalLayout")
      self.scrollArea = QtWidgets.QScrollArea(self.global_frame)
      self.scrollArea.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
      self.scrollArea.setStyleSheet("border: 0px;\nbackground-color: rgba(0, 0, 0, 0);")
      self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
      self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.scrollArea.setWidgetResizable(True)
      self.scrollArea.setObjectName("scrollArea")
      self.scrollAreaWidgetContents = QtWidgets.QWidget()
      self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 807, 10018))
      self.scrollAreaWidgetContents.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
      self.scrollAreaWidgetContents.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
      self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
      self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
      self.verticalLayout_2.setObjectName("verticalLayout_2")
      
      self.main_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
      self.main_frame.setMinimumSize(QtCore.QSize(0, 10000000))
      self.main_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
      self.main_frame.setStyleSheet("background-color: rgb(20, 28, 36);")
      self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self.main_frame.setObjectName("main_frame")
      self.add_account_title = QtWidgets.QLabel(self.main_frame)
      self.add_account_title.setGeometry(QtCore.QRect(0, 120, 820, 110))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.add_account_title.setFont(font)
      self.add_account_title.setStyleSheet("color: white;")
      self.add_account_title.setObjectName("add_account_title")
      self.add_account_emoji = QtWidgets.QLabel(self.main_frame)
      self.add_account_emoji.setGeometry(QtCore.QRect(0, 190, 820, 60))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(64)
      self.add_account_emoji.setFont(font)
      self.add_account_emoji.setStyleSheet("color: white; background-color: rgba(255, 255, 255, 0);")
      self.add_account_emoji.setObjectName("add_account_emoji")

      self.verticalLayout_2.addWidget(self.main_frame)
      self.scrollArea.setWidget(self.scrollAreaWidgetContents)
      self.verticalLayout.addWidget(self.scrollArea)
      self._buttons_frame = QtWidgets.QFrame(self.centralwidget)
      self._buttons_frame.setGeometry(QtCore.QRect(10, 390, 801, 61))
      self._buttons_frame.setStyleSheet("background-color: rgb(20, 28, 36);")
      self._buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self._buttons_frame.setObjectName("_buttons_frame")
      self.add_account_button = QtWidgets.QPushButton(self._buttons_frame)
      self.add_account_button.setGeometry(QtCore.QRect(10, 10, 190, 41))
      self.add_account_button.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.add_account_button.setFont(font)
      self.add_account_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.add_account_button.setStyleSheet("QPushButton {\nborder: 2px solid rgb(39,65,100);\nbackground-color: transparent;\ncolor: rgb(255, 255, 255);\ntext-align: center;\nborder-top-left-radius: 10px;\nborder-bottom-left-radius: 10px;\n}\nQPushButton::hover{\nbackground-color: rgb(39,65,100);\n}")
      self.add_account_button.setIconSize(QtCore.QSize(30, 1000))
      self.add_account_button.setObjectName("add_account_button")
      self.run_accounts_button = QtWidgets.QPushButton(self._buttons_frame)
      self.run_accounts_button.setGeometry(QtCore.QRect(200, 10, 200, 41))
      self.run_accounts_button.setMaximumSize(QtCore.QSize(10000, 10000))
      self.run_accounts_button.setFont(font)
      self.run_accounts_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.run_accounts_button.setStyleSheet("QPushButton {\nborder: 2px solid rgb(39,65,100);\nbackground-color: transparent;\ncolor: rgb(255, 255, 255);\ntext-align: center;\nborder-left: 0px\n}\nQPushButton::hover{\nbackground-color: rgb(39,65,100);\n}\n")
      self.run_accounts_button.setIconSize(QtCore.QSize(30, 1000))
      self.run_accounts_button.setObjectName("run_accounts_button")
      self.delete_accounts_button = QtWidgets.QPushButton(self._buttons_frame)
      self.delete_accounts_button.setGeometry(QtCore.QRect(600, 10, 190, 41))
      self.delete_accounts_button.setMaximumSize(QtCore.QSize(10000, 10000))
      self.delete_accounts_button.setFont(font)
      self.delete_accounts_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.delete_accounts_button.setStyleSheet("QPushButton {\nborder: 2px solid rgb(39,65,100);\nbackground-color: transparent;\ncolor: rgb(255, 255, 255);\n	text-align: center;\n	border-top-right-radius: 10px;\n	border-bottom-right-radius: 10px;\nborder-left: 0px\n}\nQPushButton::hover{\nbackground-color: rgb(39,65,100);\n}\n")
      self.delete_accounts_button.setIconSize(QtCore.QSize(30, 1000))
      self.delete_accounts_button.setObjectName("delete_accounts_button")
      self.load_tokens_popup_button = QtWidgets.QPushButton(self._buttons_frame)
      self.load_tokens_popup_button.setGeometry(QtCore.QRect(400, 10, 200, 41))
      self.load_tokens_popup_button.setMaximumSize(QtCore.QSize(10000, 10000))
      self.load_tokens_popup_button.setFont(font)
      self.load_tokens_popup_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.load_tokens_popup_button.setStyleSheet("QPushButton {\nborder: 2px solid rgb(39,65,100);\nbackground-color: transparent;\ncolor: rgb(255, 255, 255);\n	text-align: center;\nborder-left: 0px\n}\nQPushButton::hover{\nbackground-color: rgb(39,65,100);\n}\n")
      self.load_tokens_popup_button.setIconSize(QtCore.QSize(30, 1000))
      self.load_tokens_popup_button.setObjectName("run_accounts_button")

      self._popups_frame = QtWidgets.QFrame(self.centralwidget)
      self._popups_frame.setGeometry(QtCore.QRect(1080, 50, 501, 311))
      self._popups_frame.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
      self._popups_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self._popups_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self._popups_frame.setObjectName("_popups_frame")
      self.token_popup = QtWidgets.QFrame(self._popups_frame)
      self.token_popup.setGeometry(QtCore.QRect(1000, 0, 500, 311))
      self.token_popup.setStyleSheet("background-color:rgb(20, 28, 36);\nborder-radius: 10px;\nborder: 1px solid white;")
      self.token_popup.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.token_popup.setFrameShadow(QtWidgets.QFrame.Raised)
      self.token_popup.setObjectName("token_popup")
      self.channel_id_title = QtWidgets.QLabel(self.token_popup)
      self.channel_id_title.setGeometry(QtCore.QRect(10, 9, 101, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.channel_id_title.setFont(font)
      self.channel_id_title.setStyleSheet("color: rgb(255, 255, 255);\nborder: none;")
      self.channel_id_title.setObjectName("channel_id_title")
      self.token_title = QtWidgets.QLabel(self.token_popup)
      self.token_title.setGeometry(QtCore.QRect(10, 89, 71, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.token_title.setFont(font)
      self.token_title.setStyleSheet("color: rgb(255, 255, 255);\nborder: none;")
      self.token_title.setObjectName("token_title")
      self.add_token = QtWidgets.QPushButton(self.token_popup)
      self.add_token.setGeometry(QtCore.QRect(350, 260, 60, 40))
      self.add_token.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.add_token.setFont(font)
      self.add_token.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.add_token.setStyleSheet("QPushButton { color: rgb(255, 255, 255);text-align: center;background-color: rgb(39,65,100);border: none;}\nQPushButton::hover {background-color: rgb(60, 94, 150);}")
      self.add_token.setIconSize(QtCore.QSize(30, 1000))
      self.add_token.setObjectName("add_token")
      self.close_popup = QtWidgets.QPushButton(self.token_popup)
      self.close_popup.setGeometry(QtCore.QRect(420, 260, 70, 40))
      self.close_popup.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.close_popup.setFont(font)
      self.close_popup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.close_popup.setStyleSheet("QPushButton { color: rgb(255, 255, 255);	text-align: center;	border: 2px solid rgb(39,65,100);}\nQPushButton::hover{background-color: rgb(39,65,100);}")
      self.close_popup.setIconSize(QtCore.QSize(30, 1000))
      self.close_popup.setObjectName("close_popup")
      self.token_input = QtWidgets.QLineEdit(self.token_popup)
      self.token_input.setGeometry(QtCore.QRect(10, 120, 480, 45))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(9)
      font.setBold(False)
      font.setWeight(50)
      self.token_input.setFont(font)
      self.token_input.setWhatsThis("")
      self.token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.token_input.setEchoMode(QtWidgets.QLineEdit.Password)
      self.token_input.setObjectName("token_input")
      self.channel_id_input = QtWidgets.QLineEdit(self.token_popup)
      self.channel_id_input.setGeometry(QtCore.QRect(10, 40, 480, 45))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.channel_id_input.setFont(font)
      self.channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.channel_id_input.setEchoMode(QtWidgets.QLineEdit.Normal)
      self.channel_id_input.setObjectName("channel_id_input")
      self.validating_popup = QtWidgets.QFrame(self.token_popup)
      self.validating_popup.setGeometry(QtCore.QRect(1000, 0, 501, 311))
      self.validating_popup.setStyleSheet("background-color:  rgba(20, 28, 36, 100);\nborder-radius: 10px;")
      self.validating_popup.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.validating_popup.setFrameShadow(QtWidgets.QFrame.Raised)
      self.validating_popup.setObjectName("validating_popup")
      self.validating_title = QtWidgets.QLabel(self.validating_popup)
      self.validating_title.setGeometry(QtCore.QRect(0, 0, 500, 311))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.validating_title.setFont(font)
      self.validating_title.setStyleSheet("color: white;\ntext-align: center;")
      self.validating_title.setObjectName("validating_title")
      self.coming_soon_frame = QtWidgets.QFrame(self.validating_popup)
      self.coming_soon_frame.setGeometry(QtCore.QRect(1000, 90, 481, 140))
      self.coming_soon_frame.setStyleSheet("background-color: rgb(27, 27, 27);\ncolor: white;\nborder: 1px solid white;\nborder-radius: 10px;")
      self.coming_soon_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.coming_soon_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      self.coming_soon_frame.setObjectName("coming_soon_frame")
      self.coming_soon_title = QtWidgets.QLabel(self.coming_soon_frame)
      self.coming_soon_title.setGeometry(QtCore.QRect(10, 20, 450, 60))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(48)
      self.coming_soon_title.setFont(font)
      self.coming_soon_title.setStyleSheet("border: 0px;")
      self.coming_soon_title.setObjectName("coming_soon_title")
      self.coming_soon_close_button = QtWidgets.QPushButton(self.coming_soon_frame)
      self.coming_soon_close_button.setGeometry(QtCore.QRect(200, 80, 70, 40))
      self.coming_soon_close_button.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(12)
      font.setBold(True)
      font.setWeight(75)
      self.coming_soon_close_button.setFont(font)
      self.coming_soon_close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.coming_soon_close_button.setStyleSheet("QPushButton {\n    background-color: rgb(43, 43, 43);\n    color: rgb(255, 255, 255);\n    text-align: center;\n    border: solid rgb(43, 43, 43);\n\n}\nQPushButton::hover{\n    background-color: rgb(59, 59, 59);\n}\nQPushButton:pressed {\n    font-size: 15px;\n    font-family: Century Gothic;\n    background-color: rgb(43, 43, 43);\n}\n")
      self.coming_soon_close_button.setIconSize(QtCore.QSize(30, 1000))
      self.coming_soon_close_button.setObjectName("close_button")
      self.webhook_url_title = QtWidgets.QLabel(self.token_popup)
      self.webhook_url_title.setGeometry(QtCore.QRect(10, 169, 121, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.webhook_url_title.setFont(font)
      self.webhook_url_title.setStyleSheet("color: rgb(255, 255, 255);\nborder: none;")
      self.webhook_url_title.setObjectName("webhook_url_title")
      self.webhook_url_input = QtWidgets.QLineEdit(self.token_popup)
      self.webhook_url_input.setGeometry(QtCore.QRect(10, 200, 480, 45))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(9)
      self.webhook_url_input.setFont(font)
      self.webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.webhook_url_input.setEchoMode(QtWidgets.QLineEdit.Password)
      self.webhook_url_input.setObjectName("webhook_url_input")

      self.editing_token_popup = QtWidgets.QFrame(self._popups_frame)
      self.editing_token_popup.setGeometry(QtCore.QRect(1000, 0, 500, 311))
      self.editing_token_popup.setStyleSheet("background-color:rgb(20, 28, 36);\nborder-radius: 10px;\nborder: 1px solid white;")
      self.editing_token_popup.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.editing_token_popup.setFrameShadow(QtWidgets.QFrame.Raised)
      self.editing_token_popup.setObjectName("token_popup")
      self.editing_channel_id_title = QtWidgets.QLabel(self.editing_token_popup)
      self.editing_channel_id_title.setGeometry(QtCore.QRect(10, 9, 101, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.editing_channel_id_title.setFont(font)
      self.editing_channel_id_title.setStyleSheet("color: rgb(255, 255, 255);\nborder: 0px;\ntext-align:left;")
      self.editing_channel_id_title.setObjectName("editing_channel_id_title")
      self.editing_token_title = QtWidgets.QLabel(self.editing_token_popup)
      self.editing_token_title.setGeometry(QtCore.QRect(10, 89, 71, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.editing_token_title.setFont(font)
      self.editing_token_title.setStyleSheet("color: rgb(255, 255, 255);\nborder: 0px;\ntext-align:left;")
      self.editing_token_title.setObjectName("token_title")
      self.editing_token = QtWidgets.QPushButton(self.editing_token_popup)
      self.editing_token.setGeometry(QtCore.QRect(350, 260, 60, 40))
      self.editing_token.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.editing_token.setFont(font)
      self.editing_token.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.editing_token.setStyleSheet("QPushButton { color: rgb(255, 255, 255);text-align: center;background-color: rgb(39,65,100);border: none;}\nQPushButton::hover {background-color: rgb(60, 94, 150);}")
      self.editing_token.setIconSize(QtCore.QSize(30, 1000))
      self.editing_token.setObjectName("add_token")
      self.editing_close_popup = QtWidgets.QPushButton(self.editing_token_popup)
      self.editing_close_popup.setGeometry(QtCore.QRect(420, 260, 70, 40))
      self.editing_close_popup.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(16)
      font.setBold(True)
      font.setWeight(75)
      self.editing_close_popup.setFont(font)
      self.editing_close_popup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.editing_close_popup.setStyleSheet("QPushButton { color: rgb(255, 255, 255);	text-align: center;	border: 2px solid rgb(39,65,100);}\nQPushButton::hover{background-color: rgb(39,65,100);}")
      self.editing_close_popup.setIconSize(QtCore.QSize(30, 1000))
      self.editing_close_popup.setObjectName("close_popup")
      self.editing_token_input = QtWidgets.QLineEdit(self.editing_token_popup)
      self.editing_token_input.setGeometry(QtCore.QRect(10, 120, 480, 45))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(9)
      font.setBold(False)
      font.setWeight(50)
      self.editing_token_input.setFont(font)
      self.editing_token_input.setWhatsThis("")
      self.editing_token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.editing_token_input.setEchoMode(QtWidgets.QLineEdit.Password)
      self.editing_token_input.setObjectName("token_input")
      self.editing_channel_id_input = QtWidgets.QLineEdit(self.editing_token_popup)
      self.editing_channel_id_input.setGeometry(QtCore.QRect(10, 40, 480, 45))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(13)
      self.editing_channel_id_input.setFont(font)
      self.editing_channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.editing_channel_id_input.setEchoMode(QtWidgets.QLineEdit.Normal)
      self.editing_channel_id_input.setObjectName("editing_channel_id_input")
      self.editing_webhook_url_title = QtWidgets.QLabel(self.editing_token_popup)
      self.editing_webhook_url_title.setGeometry(QtCore.QRect(10, 169, 121, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.editing_webhook_url_title.setFont(font)
      self.editing_webhook_url_title.setStyleSheet("color: rgb(255, 255, 255);\nborder: none;")
      self.editing_webhook_url_title.setObjectName("editing_webhook_url_title")
      self.editing_webhook_url_input = QtWidgets.QLineEdit(self.editing_token_popup)
      self.editing_webhook_url_input.setGeometry(QtCore.QRect(10, 200, 480, 45))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(9)
      self.editing_webhook_url_input.setFont(font)
      self.editing_webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.editing_webhook_url_input.setEchoMode(QtWidgets.QLineEdit.Password)
      self.editing_webhook_url_input.setObjectName("editing_webhook_url_input")
      self.editing_validating_popup = QtWidgets.QFrame(self.editing_token_popup)
      self.editing_validating_popup.setGeometry(QtCore.QRect(1000, 0, 501, 311))
      self.editing_validating_popup.setStyleSheet("background-color:  rgba(20, 28, 36, 100);\nborder-radius: 10px;")
      self.editing_validating_popup.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.editing_validating_popup.setFrameShadow(QtWidgets.QFrame.Raised)
      self.editing_validating_popup.setObjectName("editing_validating_popup")
      self.editing_validating_title = QtWidgets.QLabel(self.editing_validating_popup)
      self.editing_validating_title.setGeometry(QtCore.QRect(0, 0, 500, 311))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      self.editing_validating_title.setFont(font)
      self.editing_validating_title.setStyleSheet("color: white;\ntext-align: center;")
      self.editing_validating_title.setObjectName("editing_validating_title")

      self.add_account_title.raise_()
      self.add_account_emoji.raise_()
      self.add_account_button.raise_()
      self.run_accounts_button.raise_()
      self.load_tokens_popup_button.raise_()
      self.delete_accounts_button.raise_()
      # self.validating_popup.raise_()
      # self.editing_validating_popup.raise_()
      # self.token_popup.raise_()

      self.load_tokens_popup = QtWidgets.QFrame(self.centralwidget)
      self.load_tokens_popup.setGeometry(QtCore.QRect(1500, 50, 541, 311))
      self.load_tokens_popup.setStyleSheet("""QFrame {
	background-color:rgb(20, 28, 36);
	border-radius: 10px;
	border: 1px solid white;
}
QScrollBar:vertical {
	border: none;
    background-color: transparent;
    width: 12px;
    margin: 0px 0 0px 0;
	border-radius: 0px;
 }

/*  HANDLE BAR VERTICAL */
QScrollBar::handle:vertical {
	background-color: rgb(60, 94, 150);
	border-radius: 6px;
}

/* BTN TOP - SCROLLBAR */
QScrollBar::sub-line:vertical {
	border-radius: 0px;
	background-color: rgba(23,23,23,255);
}

/* BTN BOTTOM - SCROLLBAR */
QScrollBar::add-line:vertical {
	border-radius: 0px;
	background-color: rgba(23,23,23,255);
}
/* RESET ARROW */
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
	background-color: rgba(23,23,23,255);
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	background-color: rgba(23,23,23,255);
}""")
      self.load_tokens_popup.setFrameShape(QtWidgets.QFrame.StyledPanel)
      self.load_tokens_popup.setFrameShadow(QtWidgets.QFrame.Raised)
      self.load_tokens_popup.setObjectName("load_tokens_popup")
      self.mass_tokens_input = QtWidgets.QTextEdit(self.load_tokens_popup)
      self.mass_tokens_input.setGeometry(QtCore.QRect(10, 110, 521, 171))
      font = QtGui.QFont(); font.setFamily("Cascadia Mono"); font.setPointSize(8); font.setBold(False); font.setWeight(50)
      self.mass_tokens_input.setFont(font)
      self.mass_tokens_input.setStyleSheet("""QTextEdit {
	border: 2px solid rgb(60, 94, 150);
	border-radius: 5px;
	background-color: rgba(23,23,23,255);
	padding: 3px;
	color: white;
}
QToolTip {
	background-color: rgb(27, 27, 27);
	color: white;
	text-align: cetner;
	border: 2px solid black;
	font-family: Century Gothic;
}
""")
      self.mass_tokens_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
      self.mass_tokens_input.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.mass_tokens_input.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
      self.mass_tokens_input.setAcceptRichText(False)
      self.mass_tokens_input.setObjectName("mass_tokens_input")
      self.format_text = QtWidgets.QLabel(self.load_tokens_popup)
      self.format_text.setGeometry(QtCore.QRect(10, 280, 521, 31))
      font = QtGui.QFont(); font.setFamily("Cascadia Mono")
      self.format_text.setFont(font)
      self.format_text.setStyleSheet("border: 0px;\nbackground-color: transparent;\npadding-bottom: 3px;")
      self.format_text.setObjectName("format_text")
      self.default_channel_label = QtWidgets.QTextEdit(self.load_tokens_popup)
      self.default_channel_label.setGeometry(QtCore.QRect(10, 20, 171, 31))
      font = QtGui.QFont(); font.setFamily("Cascadia Mono"); font.setPointSize(8); font.setBold(False); font.setWeight(50)
      self.default_channel_label.setFont(font)
      self.default_channel_label.setStyleSheet("""QTextEdit {
	border: 2px solid rgb(60, 94, 150);
	border-radius: 5px;
	background-color: rgba(23,23,23,255);
	color: white;
	border-right: none;
	border-top-right-radius: 0px;
	border-bottom-right-radius: 0px;
}
""")
      self.default_channel_label.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.default_channel_label.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.default_channel_label.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
      self.default_channel_label.setReadOnly(True)
      self.default_channel_label.setAcceptRichText(False)
      self.default_channel_label.setObjectName("default_channel_label")
      self.default_webhook_label = QtWidgets.QTextEdit(self.load_tokens_popup)
      self.default_webhook_label.setGeometry(QtCore.QRect(10, 60, 171, 31))
      font = QtGui.QFont(); font.setFamily("Cascadia Mono"); font.setPointSize(8); font.setBold(False); font.setWeight(50)
      self.default_webhook_label.setFont(font)
      self.default_webhook_label.setStyleSheet("""QTextEdit {
	border: 2px solid rgb(60, 94, 150);
	border-radius: 5px;
	background-color: rgba(23,23,23,255);
	color: white;
	border-right: none;
	border-top-right-radius: 0px;
	border-bottom-right-radius: 0px;
}
""")
      self.default_webhook_label.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.default_webhook_label.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.default_webhook_label.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
      self.default_webhook_label.setReadOnly(True)
      self.default_webhook_label.setAcceptRichText(False)
      self.default_webhook_label.setObjectName("default_webhook_label")
      self.default_webhook_input = QtWidgets.QLineEdit(self.load_tokens_popup)
      self.default_webhook_input.setGeometry(QtCore.QRect(180, 60, 351, 31))
      self.default_webhook_input.setStyleSheet("""QLineEdit {
	border: 2px solid rgb(60, 94, 150);
	border-radius: 5px;
	background-color: rgba(23,23,23,255);
	color: white;
	border-top-left-radius: 0px;
	border-bottom-left-radius: 0px;
	padding-left: 2px;
}

QToolTip {
	background-color: rgb(27, 27, 27);
	color: white;
	text-align: cetner;
	border: 2px solid black;
	font-family: Century Gothic;
}""")
      self.default_webhook_input.setEchoMode(QtWidgets.QLineEdit.Password)
      self.default_webhook_input.setObjectName("default_webhook_input")
      self.default_channel_input = QtWidgets.QLineEdit(self.load_tokens_popup)
      self.default_channel_input.setGeometry(QtCore.QRect(180, 20, 191, 31))
      self.default_channel_input.setStyleSheet("""QLineEdit {
	border: 2px solid rgb(60, 94, 150);
	border-radius: 5px;
	background-color: rgba(23,23,23,255);
	color: white;
	border-top-left-radius: 0px;
	border-bottom-left-radius: 0px;
	padding-left: 2px;
}
""")
      self.default_channel_input.setObjectName("default_channel_input")
      self.close_tokens_popup = QtWidgets.QPushButton(self.load_tokens_popup)
      self.close_tokens_popup.setGeometry(QtCore.QRect(480, 20, 51, 31))
      self.close_tokens_popup.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(10); font.setBold(True); font.setWeight(75)
      self.close_tokens_popup.setFont(font)
      self.close_tokens_popup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.close_tokens_popup.setStyleSheet("""QPushButton {
	color: rgb(255, 255, 255);
	text-align: center;
	border: 2px solid rgb(39,65,100);
	border-radius: 5px;
}
QPushButton::hover{
	background-color: rgb(39,65,100);
}
""")
      self.close_tokens_popup.setIconSize(QtCore.QSize(30, 1000))
      self.close_tokens_popup.setObjectName("close_tokens_popup")
      self.load_tokens_button = QtWidgets.QPushButton(self.load_tokens_popup)
      self.load_tokens_button.setGeometry(QtCore.QRect(420, 20, 51, 31))
      self.load_tokens_button.setMaximumSize(QtCore.QSize(10000, 10000))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(10); font.setBold(True); font.setWeight(75)
      self.load_tokens_button.setFont(font)
      self.load_tokens_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      self.load_tokens_button.setStyleSheet("""QPushButton {
	color: rgb(255, 255, 255);
	text-align: center;
	background-color: rgb(39,65,100);
	border: none;
	border-radius: 5px;
}
QPushButton::hover {
	background-color: rgb(60, 94, 150);
}
""")
      self.load_tokens_button.setIconSize(QtCore.QSize(30, 1000))
      self.load_tokens_button.setObjectName("load_tokens_button")

      
      # self.load_tokens_popup.raise_()
      self.mass_tokens_input.raise_()
      self.format_text.raise_()
      self.default_channel_label.raise_()
      self.default_webhook_label.raise_()
      self.default_webhook_input.raise_()
      self.default_channel_input.raise_()
      MultipleAccounts.setCentralWidget(self.centralwidget)

      to_hide = [
        self.token_popup,
        self.editing_token_popup,
        self.validating_popup,
        self.editing_validating_popup,
        self.coming_soon_frame,
        self.load_tokens_popup,
      ]
      for item in to_hide:
        item.hide()

      self.add_account_button.clicked.connect(lambda: self.show_account_popup())
      self.run_accounts_button.clicked.connect(lambda: self.run_or_pause())
      self.load_tokens_popup_button.clicked.connect(lambda: self.show_load_tokens_popup())
      self.delete_accounts_button.clicked.connect(lambda: self.delete_accounts())
      self.token_input.textChanged[str].connect(lambda: self.newline_gay())
      self.editing_token_input.textChanged[str].connect(lambda: self.newline_gay())
      self.add_token.clicked.connect(lambda: self.adding_token_process())
      self.close_popup.clicked.connect(lambda: self.close_token_popup())
      self.coming_soon_close_button.clicked.connect(lambda: self.close_coming_soon())
      self.editing_token.clicked.connect(lambda: self.editing_info_process())
      self.editing_close_popup.clicked.connect(lambda: self.close_token_popup())
      self.load_tokens_button.clicked.connect(lambda: self.load_tokens())
      self.close_tokens_popup.clicked.connect(lambda: self.close_load_tokens_popup())
      self.channel_id_input.textChanged.connect(lambda: self.only_integers(self.channel_id_input))
      self.editing_channel_id_input.textChanged.connect(lambda: self.only_integers(self.editing_channel_id_input))
      self.default_channel_input.textChanged.connect(lambda: self.only_integers(self.default_channel_input))

      self.add_account_emoji.hide()
      self.load_accounts()
      self.retranslateUi(MultipleAccounts)
      QtCore.QMetaObject.connectSlotsByName(MultipleAccounts)

    def show_account_logs(self, account_id):
      from threading import Thread
      t1 = Thread(target = view_account_logs, args = [account_id])
      t1.daemon = True
      t1.start()

    def globalize_settings(self, item):
      from utils.alt_handler_assist import get_account_settings, update_account_settings
      from utils.notifs import notification_messagebox

      father = item.parent().parent()
      main_account_id = int(shadow.internal["config"]['widget_values'][father]["account_id"])
      main_settings = get_account_settings(main_account_id)
      main_username = shadow.internal["config"]['widget_values'][father]["account_username"]
      for widget in shadow.internal["config"]['account_widgets']:
        if widget != father:
          secondary_account_id = shadow.internal["config"]['widget_values'][widget]["account_id"]
          secondary_settings = get_account_settings(secondary_account_id)
          secondary_settings['config'] = main_settings['config']
          secondary_settings['powerups'] = main_settings['powerups']
          secondary_settings['customization'] = main_settings['customization']

          update_account_settings(secondary_account_id, secondary_settings)
      
      return notification_messagebox(shadow.internal["config"]["tray_icon"], "Settings globalized", f"All other accounts now have the same settings as the account \"{main_username}\".")

    @asyncSlot()
    async def load_tokens(self):
      from utils.notifs import critical_messagebox
      
      if len(self.mass_tokens_input.toPlainText().replace(' ', '')) == 0:
        return critical_messagebox(shadow.internal["config"]["tray_icon"], title = "Action denied", text = "You need to add some tokens to the big input box first before attempting to load them. Consider clicking the \"CLOSE\" button if you want to close the popup.")
      if len(self.mass_tokens_input.toPlainText().replace(' ', '').split('\n')) > 50:
        return critical_messagebox(shadow.internal["config"]["tray_icon"], title = "Action denied", text = "Maximum number of accounts to be added at once is 50.")

      default_channel_id = self.default_channel_input.text()
      default_webhook_url = self.default_webhook_input.text()
      all_tokens_data = self.mass_tokens_input.toPlainText()
      accounts_data = {}
      
      for index, line in enumerate(all_tokens_data.split('\n'), 1):
        if len(line) == 0:
          continue
        if line.count(':') == 0:
          if len(default_channel_id.replace(' ', '')) == 0:
            return critical_messagebox(shadow.internal["config"]["tray_icon"], title = "Invalid data", text = f"The line {index} seems to not have a channel ID separated with a \":\", consider adding one or setting up a default channel ID.")
          accounts_data[line] = default_channel_id
        
        elif line.count(':') == 1:
          try:
            accounts_data[line.split(':')[0]] = int(line.split(':')[1])
          except ValueError:
            return critical_messagebox(shadow.internal["config"]["tray_icon"], title = "Invalid data", text = f"The line {index} seems to not have non-numerical characters set as the channel ID. See the format below for better understanding of how it works.")
          except:
            if len(default_channel_id.replace(' ', '')) == 0:
              return critical_messagebox(shadow.internal["config"]["tray_icon"], title = "Invalid data", text = f"The line {index} seems to not have a channel ID separated with a \":\", consider adding one or setting up a default channel ID.")
            accounts_data[line.split(':')[0]] = default_channel_id
        
        elif line.count(':') == 2:
          try:
            accounts_data[line.split(':')[0]] = [int(line.split(':')[1]), line.split(':')[2]]
          except ValueError:
            return critical_messagebox(shadow.internal["config"]["tray_icon"], title = "Invalid data", text = f"The line {index} seems to not have non-numerical characters set as the channel ID. See the format below for better understanding of how it works.")
        
        else:
          return critical_messagebox(shadow.internal["config"]["tray_icon"], title = "Invalid data", text = f"The line {index} seems to not be following the correct format. See the format below for better understanding of how it works.")

      for token, channel_id in accounts_data.items():
        state = self.mass_token_interal_adding(token, channel_id, default_webhook_url if len(default_webhook_url.replace(' ', '')) > 0 else None)
      
      self.close_load_tokens_popup()

    def only_integers(self, item):
      numbers = ''.join(c for c in item.text() if c.isnumeric())
      item.setText(numbers)

    def close_load_tokens_popup(self):
      try:
        self._popups_frame.setGeometry(QtCore.QRect(1800, 50, 501, 311))
        self.load_tokens_popup.setGeometry(QtCore.QRect(1500, 50, 541, 311))
        self.load_tokens_popup.hide()
        self.load_tokens_popup.destroy()
        self.mass_tokens_input.setText("")
        self.default_webhook_input.setText("")
        self.default_channel_input.setText("")
      except:
        pass

    def show_load_tokens_popup(self):
      self._popups_frame.setGeometry(QtCore.QRect(180, 50, 501, 311))
      self.load_tokens_popup.setGeometry(QtCore.QRect(150, 50, 541, 311))
      self.load_tokens_popup.show()
      self.load_tokens_popup.raise_()

    def show_coming_soon(self):
      self.coming_soon_frame.setGeometry(QtCore.QRect(10, 90, 481, 140))
      self.coming_soon_frame.show()
      self.coming_soon_frame.raise_()

    def show_alt_window(self, account_id):
      from account_gui import AltGUI
      
      self.AltWindow = QtWidgets.QMainWindow()
      self.ui = AltGUI(int(account_id), shadow.internal["config"]["tray_icon"], messenger)
      self.ui.setupUi(self.AltWindow)
      self.icon = QtGui.QIcon(iconFromBase64(logo_b64))
      self.AltWindow.setWindowIcon(self.icon)
      self.AltWindow.setFixedSize(996, 481)
      self.font = QtGui.QFont("Century Gothic")
      self.AltWindow.setFont(self.font)
      self.AltWindow.setWindowModality(QtCore.Qt.ApplicationModal)
      self.AltWindow.show()

    def show_account_popup(self):
      self._popups_frame.setGeometry(QtCore.QRect(180, 50, 501, 311))
      self.token_popup.setGeometry(QtCore.QRect(0, 0, 500, 311))
      self.token_popup.show()
      self.token_popup.raise_()

    @asyncSlot()
    async def load_accounts(self):
      from utils.useful import darkend
      from utils.alt_handler_assist import get_all_accounts_data
      import asyncio
      
      all_accounts_data = get_all_accounts_data()
      
      if all_accounts_data is None or len(all_accounts_data) == 0:
        self.add_account_title.setText(new_add_account_title_text('Add an account below'))
        self.add_account_emoji.show()
        return darkend("No accounts saved found.")
      
      for token_key, items_value in all_accounts_data.items():
        # darkend(f"Checking the token {token_key}.")
        self.internally_adding_token_process(token_key, items_value)
        await asyncio.sleep(0.5)
      
      await asyncio.sleep(1.5)
      if shadow.internal["config"]['accounts_added_at_startup'] == 0:
        self.add_account_title.setText(new_add_account_title_text('Add an account below'))
        self.add_account_emoji.show()
        return darkend("No accounts were added.")

    def close_coming_soon(self):
      self.coming_soon_frame.hide()

    def delete_accounts(self, _account_id = None):
      from utils.useful import error
      from utils.notifs import notification_messagebox
      import os
            
      appdata = os.getenv('APPDATA')
      alt_handler_directory = f"{appdata}\\Darkend v1\\Darkend Alt Handler"
      
      if len(shadow.internal["config"]['account_widgets']) == 0:
        return notification_messagebox(shadow.internal["config"]["tray_icon"], "No accounts added", "There is no accounts to delete.")
      
      if _account_id is None:
        for widget in shadow.internal["config"]['account_widgets']:
          account_id = int(shadow.internal["config"]['widget_values'][widget]["account_id"]) 
          try:
            messenger.internal[account_id]["crash"] = True
          except:
            messenger.internal[account_id] = {"crash": False}
            messenger.internal[account_id]["crash"] = True
          try:
            os.remove(f"{alt_handler_directory}\\{account_id}.json")
          except Exception as e:
            error(e)
          
          widget.hide()
          widget.deleteLater()
          widget = None
      else:
        for widget in shadow.internal["config"]['account_widgets']:
          if shadow.internal["config"]['widget_values'][widget]["account_id"] == _account_id:
            widget.hide()
            widget.deleteLater()
            widget = None
            break
        try:
          messenger.internal[_account_id]["crash"] = True
        except:
          messenger.internal[_account_id] = {"crash": False}
          messenger.internal[_account_id]["crash"] = True
        try:
          os.remove(f"{alt_handler_directory}\\{_account_id}.json")
        except Exception as e:
          error(e)
      
      if _account_id is None:
        shadow.internal["config"]['bots_running'] = None
        shadow.internal["config"]['account_widgets'] = []
        shadow.internal["config"]['widget_values'] = {}
        shadow.internal["config"]['last_height'] = 10

        self.add_account_title.setText(new_add_account_title_text('Add an account below'))
        self.add_account_title.show()
        self.add_account_emoji.show()
        self.run_accounts_button.setText("RUN ACCOUNTS")

        notification_messagebox(shadow.internal["config"]["tray_icon"], "Accounts Deleted", "All accounts have been deleted.")

    def delete_account(self, item):
      import os
      
      appdata = os.getenv('APPDATA')
      alt_handler_directory = f"{appdata}\\Darkend v1\\Darkend Alt Handler"
      acc_widgets = shadow.internal["config"]['account_widgets']
      father = item.parent().parent()
      account_id = int(shadow.internal["config"]['widget_values'][father]["account_id"])
      self.delete_accounts(account_id)

      if len(shadow.internal["config"]["account_widgets"]) > 1 and shadow.internal["config"]['last_height'] >= 70:
        shadow.internal["config"]['last_height'] = shadow.internal["config"]['last_height']-60
      else:
        shadow.internal["config"]['last_height'] = 10

      if len(acc_widgets) > 0:
        for item_ in acc_widgets[acc_widgets.index(father):9999]:
          rect_data = item_.geometry()
          x = rect_data.x()
          y = rect_data.y()
          w = rect_data.width()
          h = rect_data.height()
          item_.setGeometry(x, y-60, w, h)

      acc_widgets.remove(acc_widgets[acc_widgets.index(father)])
      item.parent().parent().hide()
      item.deleteLater()
      item = None

      try:
        os.remove(f'{alt_handler_directory}\\{account_id}.json')
      except:
        pass

      try:
        shadow.internal["config"]["account_widgets"].remove(father)
        shadow.internal["config"]['widget_values'].remove(father)
      except:
        pass

      if len(shadow.internal["config"]["account_widgets"]) == 0:
        self.add_account_title.show()
        self.add_account_title.setText(new_add_account_title_text('Add an account below'))
        self.add_account_emoji.show()
        shadow.internal["config"]['bots_running'] = None
        self.run_accounts_button.setText("RUN ACCOUNTS")

    def editing_account_popup(self, item):
      father = item.parent().parent()
      channel_id = shadow.internal["config"]['widget_values'][father]["channel_id"]
      token = shadow.internal["config"]['widget_values'][father]["token"]
      account_username = shadow.internal["config"]['widget_values'][father]["account_username"]
      webhook_url = shadow.internal["config"]['widget_values'][father]["webhook_url"]
      if len(shadow.internal["config"]['previous_webhook_url']) > 0:
        webhook_url = shadow.internal["config"]['previous_webhook_url']

      self.editing_channel_id_input.setText(str(channel_id))
      self.editing_token_input.setText(token)
      self.editing_webhook_url_input.setText(webhook_url)

      shadow.internal["config"]["previous_channel_id"] = channel_id
      shadow.internal["config"]["previous_token"] = token
      shadow.internal["config"]["previous_account_username"] = account_username
      shadow.internal["config"]["previous_father"] = father

      self._popups_frame.setGeometry(QtCore.QRect(180, 50, 501, 311))
      self.editing_token_popup.setGeometry(QtCore.QRect(0, 0, 500, 311))
      self.editing_token_popup.show()
      self.editing_token_popup.raise_()

    def close_token_popup(self):
      try:
        self.token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self._popups_frame.setGeometry(QtCore.QRect(1800, 50, 501, 311))
        self.token_popup.setGeometry(QtCore.QRect(1000, 0, 500, 311))
        self.token_popup.hide()
        self.token_popup.destroy()
        self.token_input.setText("")
        self.channel_id_input.setText("")
        
        self.editing_token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self._popups_frame.setGeometry(QtCore.QRect(1800, 50, 501, 311))
        self.editing_token_popup.setGeometry(QtCore.QRect(1000, 0, 500, 311))
        self.editing_token_popup.hide()
        self.editing_token_popup.destroy()
        self.editing_token_input.setText("")
        self.editing_channel_id_input.setText("")
      except:
        pass

    def newline_gay(self):
      self.token_input.setText(self.token_input.text().replace('\n', ''))
      self.editing_token_input.setText(self.editing_token_input.text().replace('\n', ''))
    
    @asyncSlot()
    async def mass_token_interal_adding(self, token : str, channel_id : int, webhook_url : str = None):
      import base64
      from utils.info import validate_token
      from utils.useful import error, darkend, success, misc

      validation_state, username, account_id = await validate_token(token)
      if validation_state is False: return error(f"The token {token} is invalid.")
      shadow.internal["config"]['accounts_added_at_startup'] += 1
      self.add_account_title.hide(); self.add_account_emoji.hide()
      account_frame = QtWidgets.QFrame(self.main_frame)
      
      height__ = 0
      if shadow.internal["config"]['last_height'] is None:
        # Means no element was placed
        height__ = 0
        shadow.internal["config"]['last_height'] = 0
      else:
        shadow.internal["config"]['last_height'] += 60
        height__ = shadow.internal["config"]['last_height']
      if len(shadow.internal["config"]['account_widgets']) < 1:
        shadow.internal["config"]['last_height'] = 0
        height__ = shadow.internal["config"]['last_height']
      
      account_frame.setGeometry(QtCore.QRect(0, height__, 781, 51))
      account_frame.setStyleSheet("background-color: rgb(39,65,100);;\nborder-radius: 10px;")
      account_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      account_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      account_frame.setObjectName("account_frame")
  
      account_username = QtWidgets.QLabel(account_frame)
      account_username.setGeometry(QtCore.QRect(110, 10, 321, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      account_username.setFont(font)
      account_username.setStyleSheet("color: white;")
      account_username.setObjectName("account_username")
      discord_icon = QtWidgets.QLabel(account_frame)
      discord_icon.setGeometry(QtCore.QRect(10, 10, 41, 31))
      discord_icon.setStyleSheet("border-radius: 20px;")
      discord_icon.setText("")
      discord_icon_pic = QtGui.QPixmap()
      discord_icon_pic.loadFromData(base64.b64decode(discord_icon_b64))
      discord_icon.setPixmap(discord_icon_pic)
      discord_icon.setScaledContents(True)
      discord_icon.setObjectName("discord_icon")

      buttons_frame = QtWidgets.QFrame(account_frame)
      buttons_frame.setGeometry(QtCore.QRect(570, 0, 211, 51))
      buttons_frame.setStyleSheet("QFrame {\n    background-color: rgb(60, 94, 150);\n    border-radius: 10px;\n}\nQPushButton {\n    background-color: transparent;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      buttons_frame.setObjectName("buttons_frame")

      trash_button = QtWidgets.QPushButton(buttons_frame)
      trash_button.setGeometry(QtCore.QRect(170, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(50)
      trash_button.setFont(font)
      trash_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      trash_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      trash_button.setText("")
      trash_button.setIcon(iconFromBase64(trash_icon_b64))
      trash_button.setIconSize(QtCore.QSize(25, 1000))
      trash_button.setObjectName("trash_button")

      settings_button = QtWidgets.QPushButton(buttons_frame)
      settings_button.setGeometry(QtCore.QRect(130, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(50)
      settings_button.setFont(font)
      settings_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      settings_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      settings_button.setText("")
      settings_button.setIcon(iconFromBase64(settings_icon_b64))
      settings_button.setIconSize(QtCore.QSize(25, 1000))
      settings_button.setObjectName("settings_button")
      
      edit_button = QtWidgets.QPushButton(buttons_frame)
      edit_button.setGeometry(QtCore.QRect(90, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(21); font.setBold(True); font.setWeight(50)
      edit_button.setFont(font)
      edit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      edit_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      edit_button.setText("")
      edit_button.setIcon(iconFromBase64(edit_icon_b64))
      edit_button.setIconSize(QtCore.QSize(25, 1000))
      edit_button.setObjectName("edit_button")

      globalize_settings_button = QtWidgets.QPushButton(buttons_frame)
      globalize_settings_button.setGeometry(QtCore.QRect(50, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(12); font.setBold(False); font.setWeight(50)
      globalize_settings_button.setFont(font)
      globalize_settings_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      globalize_settings_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      globalize_settings_button.setText("")
      globalize_settings_button.setIcon(iconFromBase64(globalize_icon_b64))
      globalize_settings_button.setIconSize(QtCore.QSize(25, 1000))
      globalize_settings_button.setObjectName("globalize_settings_button")

      view_logs_button = QtWidgets.QPushButton(buttons_frame)
      view_logs_button.setGeometry(QtCore.QRect(10, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(12); font.setBold(False); font.setWeight(50)
      view_logs_button.setFont(font)
      view_logs_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      view_logs_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      view_logs_button.setText("")
      view_logs_button.setIcon(iconFromBase64(view_icon_b64))
      view_logs_button.setIconSize(QtCore.QSize(25, 1000))
      view_logs_button.setObjectName("view_logs_button")
      
      trash_button.setToolTip("<html><head/><body><p align=\"center\">Delete account</p></body></html>")
      settings_button.setToolTip("<html><head/><body><p align=\"center\">Edit settings</p></body></html>")
      edit_button.setToolTip("<html><head/><body><p align=\"center\">Edit information</p></body></html>")
      globalize_settings_button.setToolTip("<html><head/><body><p align=\"center\">Globalize settings</p></body></html>")
      view_logs_button.setToolTip("<html><head/><body><p align=\"center\">Start/Pause/Resume autofarm</p></body></html>")
      
      account_username.setText(new_username_text(username))
      
      account_frame.setParent(self.main_frame)
      account_frame.show()
      account_frame.raise_()
      
      first_list = [
        account_username,
        buttons_frame,
      ]
      for item in first_list:
        item.setParent(account_frame); account_frame.raise_()
        item.show()
        item.raise_()
      
      shadow.internal["config"]['account_widgets'].append(account_frame)
      shadow.internal["config"]['widget_values'][account_frame] = {
        "channel_id" : channel_id,
        "token" : token,
        "account_username" : username,
        "account_id" : account_id,
        "webhook_url" : webhook_url,
      }

      trash_button.clicked.connect(lambda: self.delete_account(trash_button))
      edit_button.clicked.connect(lambda: self.editing_account_popup(edit_button))
      settings_button.clicked.connect(lambda: self.show_alt_window(shadow.internal["config"]['widget_values'][account_frame]["account_id"]))
      globalize_settings_button.clicked.connect(lambda: self.globalize_settings(globalize_settings_button))
      view_logs_button.clicked.connect(lambda: self.show_account_logs(account_id))
      
      create_account_file(account_id)
      data = get_account_settings(account_id)
      data["data"]["token"] = str(token)
      data["data"]["channel_id"] = channel_id
      data["data"]["account_id"] = account_id
      data["data"]["webhook_url"] = str(webhook_url)
      update_account_settings(account_id, data)
      ensure_new_keys_get_added(account_id)

    @asyncSlot()
    async def internally_adding_token_process(self, token : str, data_):
      from utils.info import validate_token
      
      from utils.useful import error, darkend, success, misc
      import base64, os

      webhook_url = data_['webhook_url']
      account_id_from_data = data_['account_id']
      appdata = os.getenv('APPDATA')
      alt_handler_directory = f"{appdata}\\Darkend v1\\Darkend Alt Handler"

      validation_state, username, account_id = await validate_token(token)
      data = get_account_settings(account_id)
      try:
        channel_id = data["data"]["channel_id"]
      except:
        try:
          os.remove(f"{alt_handler_directory}\\{account_id_from_data}.json")
        except:
          pass
        try:
          messenger.internal[account_id]["crash"] = True
        except Exception as e:
          error(f"The account with the ID {account_id} doesn't have data in `messenger`.")
        return

      if validation_state is False:
        try:
          os.remove(f"{alt_handler_directory}\\{account_id_from_data}.json")
        except Exception as e:
          error(e)
        return error(f"The token {token} is invalid.")
      
      shadow.internal["config"]['accounts_added_at_startup'] += 1
      self.add_account_title.hide()
      self.add_account_emoji.hide()
      account_frame = QtWidgets.QFrame(self.main_frame)
      
      height__ = 0
      if shadow.internal["config"]['last_height'] is None:
        # Means no element was placed
        height__ = 0
        shadow.internal["config"]['last_height'] = 0
      else:
        shadow.internal["config"]['last_height'] += 60
        height__ = shadow.internal["config"]['last_height']
      if len(shadow.internal["config"]['account_widgets']) < 1:
        shadow.internal["config"]['last_height'] = 0
        height__ = shadow.internal["config"]['last_height']
      
      account_frame.setGeometry(QtCore.QRect(0, height__, 781, 51))
      account_frame.setStyleSheet("background-color: rgb(39,65,100);;\nborder-radius: 10px;")
      account_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      account_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      account_frame.setObjectName("account_frame")
  
      account_username = QtWidgets.QLabel(account_frame)
      account_username.setGeometry(QtCore.QRect(110, 10, 321, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      account_username.setFont(font)
      account_username.setStyleSheet("color: white;")
      account_username.setObjectName("account_username")
      discord_icon = QtWidgets.QLabel(account_frame)
      discord_icon.setGeometry(QtCore.QRect(10, 10, 41, 31))
      discord_icon.setStyleSheet("border-radius: 20px;")
      discord_icon.setText("")
      discord_icon_pic = QtGui.QPixmap()
      discord_icon_pic.loadFromData(base64.b64decode(discord_icon_b64))
      discord_icon.setPixmap(discord_icon_pic)
      discord_icon.setScaledContents(True)
      discord_icon.setObjectName("discord_icon")

      buttons_frame = QtWidgets.QFrame(account_frame)
      buttons_frame.setGeometry(QtCore.QRect(570, 0, 211, 51))
      buttons_frame.setStyleSheet("QFrame {\n    background-color: rgb(60, 94, 150);\n    border-radius: 10px;\n}\nQPushButton {\n    background-color: transparent;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      buttons_frame.setObjectName("buttons_frame")

      trash_button = QtWidgets.QPushButton(buttons_frame)
      trash_button.setGeometry(QtCore.QRect(170, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(50)
      trash_button.setFont(font)
      trash_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      trash_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      trash_button.setText("")
      trash_button.setIcon(iconFromBase64(trash_icon_b64))
      trash_button.setIconSize(QtCore.QSize(25, 1000))
      trash_button.setObjectName("trash_button")

      settings_button = QtWidgets.QPushButton(buttons_frame)
      settings_button.setGeometry(QtCore.QRect(130, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(50)
      settings_button.setFont(font)
      settings_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      settings_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      settings_button.setText("")
      settings_button.setIcon(iconFromBase64(settings_icon_b64))
      settings_button.setIconSize(QtCore.QSize(25, 1000))
      settings_button.setObjectName("settings_button")
      
      edit_button = QtWidgets.QPushButton(buttons_frame)
      edit_button.setGeometry(QtCore.QRect(90, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(21); font.setBold(True); font.setWeight(50)
      edit_button.setFont(font)
      edit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      edit_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      edit_button.setText("")
      edit_button.setIcon(iconFromBase64(edit_icon_b64))
      edit_button.setIconSize(QtCore.QSize(25, 1000))
      edit_button.setObjectName("edit_button")

      globalize_settings_button = QtWidgets.QPushButton(buttons_frame)
      globalize_settings_button.setGeometry(QtCore.QRect(50, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(12); font.setBold(False); font.setWeight(50)
      globalize_settings_button.setFont(font)
      globalize_settings_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      globalize_settings_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      globalize_settings_button.setText("")
      globalize_settings_button.setIcon(iconFromBase64(globalize_icon_b64))
      globalize_settings_button.setIconSize(QtCore.QSize(25, 1000))
      globalize_settings_button.setObjectName("globalize_settings_button")

      view_logs_button = QtWidgets.QPushButton(buttons_frame)
      view_logs_button.setGeometry(QtCore.QRect(10, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(12); font.setBold(False); font.setWeight(50)
      view_logs_button.setFont(font)
      view_logs_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      view_logs_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      view_logs_button.setText("")
      view_logs_button.setIcon(iconFromBase64(view_icon_b64))
      view_logs_button.setIconSize(QtCore.QSize(25, 1000))
      view_logs_button.setObjectName("view_logs_button")
      
      trash_button.setToolTip("<html><head/><body><p align=\"center\">Delete account</p></body></html>")
      settings_button.setToolTip("<html><head/><body><p align=\"center\">Edit settings</p></body></html>")
      edit_button.setToolTip("<html><head/><body><p align=\"center\">Edit information</p></body></html>")
      globalize_settings_button.setToolTip("<html><head/><body><p align=\"center\">Globalize settings</p></body></html>")
      view_logs_button.setToolTip("<html><head/><body><p align=\"center\">Start/Pause/Resume autofarm</p></body></html>")
      
      account_username.setText(new_username_text(username))
      
      account_frame.setParent(self.main_frame)
      account_frame.show()
      account_frame.raise_()
      
      first_list = [
        account_username,
        buttons_frame,
      ]
      for item in first_list:
        item.setParent(account_frame); account_frame.raise_()
        item.show()
        item.raise_()
      
      shadow.internal["config"]['account_widgets'].append(account_frame)
      shadow.internal["config"]['widget_values'][account_frame] = {
        "channel_id" : channel_id,
        "token" : token,
        "account_username" : username,
        "account_id" : account_id,
        "webhook_url" : webhook_url,
      }

      trash_button.clicked.connect(lambda: self.delete_account(trash_button))
      edit_button.clicked.connect(lambda: self.editing_account_popup(edit_button))
      settings_button.clicked.connect(lambda: self.show_alt_window(shadow.internal["config"]['widget_values'][account_frame]["account_id"]))
      globalize_settings_button.clicked.connect(lambda: self.globalize_settings(globalize_settings_button))
      view_logs_button.clicked.connect(lambda: self.show_account_logs(account_id))

      ensure_new_keys_get_added(account_id)

    @asyncSlot()
    async def adding_token_process(self):
      from utils.info import validate_token, validate_channel, validate_hook
      from utils.notifs import critical_messagebox, notification_messagebox
      
      import base64

      token = self.token_input.text()
      channel_id = self.channel_id_input.text() # must stay here because it will be resetted later
      webhook_url = self.webhook_url_input.text()
      webhook_state = False

      if len(token) == 0:#continue from here 
        return critical_messagebox(shadow.internal["config"]["tray_icon"], "Token not supplied", "You haven't inputted a token.")

      self._popups_frame.setGeometry(QtCore.QRect(180, 50, 501, 311))
      self.validating_popup.setGeometry(QtCore.QRect(0, 0, 501, 311))
      self.validating_popup.show()

      validation_state, username, account_id = await validate_token(token)
      channel_state = await validate_channel(token, channel_id)
      if len(webhook_url) > 0 and validation_state is True:
        webhook_state = await validate_hook(token, webhook_url)

      self._popups_frame.setGeometry(QtCore.QRect(1800, 50, 501, 311))
      self.validating_popup.setGeometry(QtCore.QRect(1000, 0, 501, 311))
      self.validating_popup.hide()

      if validation_state is False:
        self.webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.token_input.setStyleSheet("border: 2px solid red;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
        return critical_messagebox(shadow.internal["config"]["tray_icon"], "Invalid Token", f"The token you've added is invalid.")
      
      if channel_state is False:
        self.token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.channel_id_input.setStyleSheet("border: 2px solid red;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
        return critical_messagebox(shadow.internal["config"]["tray_icon"], "Invalid Channel", f"The channel ID you've added is invalid.")
      
      if len(webhook_url) > 0 and validation_state is True and webhook_state is False:
        self.token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.webhook_url_input.setStyleSheet("border: 2px solid red;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
        return critical_messagebox(shadow.internal["config"]["tray_icon"], "Invalid Webhook URL", f"The Webhook URL you've added is invalid.")

      father = shadow.internal["config"]['previous_father']
      if len(webhook_url) > 0 and webhook_state is True:
        shadow.internal["config"]['previous_webhook_url'] = webhook_url

      # Checking if the token has already been added previously
      for widget in shadow.internal["config"]['account_widgets']:
        if widget != father:
          if shadow.internal["config"]['widget_values'][widget]["token"].replace('\n', '') == token.replace('\n', ''):
            self.channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
            self.token_input.setStyleSheet("border: 2px solid red;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
            return  critical_messagebox(shadow.internal["config"]["tray_icon"], "Token already added", f"There is already an account that has this token.")

      self.token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.close_token_popup()
      self.add_account_emoji.hide()
      self.add_account_title.hide()
      account_frame = QtWidgets.QFrame(self.main_frame)
      
      height__ = 0
      if shadow.internal["config"]['last_height'] is None:
        # Means no element was placed
        height__ = 0
        shadow.internal["config"]['last_height'] = 0
      else:
        shadow.internal["config"]['last_height'] += 60
        height__ = shadow.internal["config"]['last_height']
      if len(shadow.internal["config"]['account_widgets']) < 1:
        shadow.internal["config"]['last_height'] = 0
        height__ = shadow.internal["config"]['last_height']
      
      account_frame.setGeometry(QtCore.QRect(0, height__, 781, 51))
      account_frame.setStyleSheet("background-color: rgb(39,65,100);;\nborder-radius: 10px;")
      account_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      account_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      account_frame.setObjectName("account_frame")
  
      account_username = QtWidgets.QLabel(account_frame)
      account_username.setGeometry(QtCore.QRect(110, 10, 321, 31))
      font = QtGui.QFont()
      font.setFamily("Century Gothic")
      font.setPixelSize(43)
      account_username.setFont(font)
      account_username.setStyleSheet("color: white;")
      account_username.setObjectName("account_username")
      discord_icon = QtWidgets.QLabel(account_frame)
      discord_icon.setGeometry(QtCore.QRect(10, 10, 41, 31))
      discord_icon.setStyleSheet("border-radius: 20px;")
      discord_icon.setText("")
      discord_icon_pic = QtGui.QPixmap()
      discord_icon_pic.loadFromData(base64.b64decode(discord_icon_b64))
      discord_icon.setPixmap(discord_icon_pic)
      discord_icon.setScaledContents(True)
      discord_icon.setObjectName("discord_icon")

      buttons_frame = QtWidgets.QFrame(account_frame)
      buttons_frame.setGeometry(QtCore.QRect(570, 0, 211, 51))
      buttons_frame.setStyleSheet("QFrame {\n    background-color: rgb(60, 94, 150);\n    border-radius: 10px;\n}\nQPushButton {\n    background-color: transparent;\n}\nQToolTip {\n    background-color: rgb(27, 27, 27);\n    color: white;\n    text-align: cetner;\n    border: 2px solid black;\n    font-family: Century Gothic;\n}")
      buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
      buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
      buttons_frame.setObjectName("buttons_frame")

      trash_button = QtWidgets.QPushButton(buttons_frame)
      trash_button.setGeometry(QtCore.QRect(170, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(50)
      trash_button.setFont(font)
      trash_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      trash_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      trash_button.setText("")
      trash_button.setIcon(iconFromBase64(trash_icon_b64))
      trash_button.setIconSize(QtCore.QSize(25, 1000))
      trash_button.setObjectName("trash_button")

      settings_button = QtWidgets.QPushButton(buttons_frame)
      settings_button.setGeometry(QtCore.QRect(130, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(16); font.setBold(True); font.setWeight(50)
      settings_button.setFont(font)
      settings_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      settings_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      settings_button.setText("")
      settings_button.setIcon(iconFromBase64(settings_icon_b64))
      settings_button.setIconSize(QtCore.QSize(25, 1000))
      settings_button.setObjectName("settings_button")
      
      edit_button = QtWidgets.QPushButton(buttons_frame)
      edit_button.setGeometry(QtCore.QRect(90, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPixelSize(21); font.setBold(True); font.setWeight(50)
      edit_button.setFont(font)
      edit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      edit_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      edit_button.setText("")
      edit_button.setIcon(iconFromBase64(edit_icon_b64))
      edit_button.setIconSize(QtCore.QSize(25, 1000))
      edit_button.setObjectName("edit_button")

      globalize_settings_button = QtWidgets.QPushButton(buttons_frame)
      globalize_settings_button.setGeometry(QtCore.QRect(50, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(12); font.setBold(False); font.setWeight(50)
      globalize_settings_button.setFont(font)
      globalize_settings_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      globalize_settings_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      globalize_settings_button.setText("")
      globalize_settings_button.setIcon(iconFromBase64(globalize_icon_b64))
      globalize_settings_button.setIconSize(QtCore.QSize(25, 1000))
      globalize_settings_button.setObjectName("globalize_settings_button")

      view_logs_button = QtWidgets.QPushButton(buttons_frame)
      view_logs_button.setGeometry(QtCore.QRect(10, 10, 31, 31))
      font = QtGui.QFont(); font.setFamily("Century Gothic"); font.setPointSize(12); font.setBold(False); font.setWeight(50)
      view_logs_button.setFont(font)
      view_logs_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      view_logs_button.setStyleSheet("border-radius: 1px;\ntext-align: center;")
      view_logs_button.setText("")
      view_logs_button.setIcon(iconFromBase64(view_icon_b64))
      view_logs_button.setIconSize(QtCore.QSize(25, 1000))
      view_logs_button.setObjectName("view_logs_button")
      
      trash_button.setToolTip("<html><head/><body><p align=\"center\">Delete account</p></body></html>")
      settings_button.setToolTip("<html><head/><body><p align=\"center\">Edit settings</p></body></html>")
      edit_button.setToolTip("<html><head/><body><p align=\"center\">Edit information</p></body></html>")
      globalize_settings_button.setToolTip("<html><head/><body><p align=\"center\">Globalize settings</p></body></html>")
      view_logs_button.setToolTip("<html><head/><body><p align=\"center\">Start/Pause/Resume autofarm</p></body></html>")
      
      account_username.setText(new_username_text(username))
      
      account_frame.setParent(self.main_frame)
      account_frame.show()
      account_frame.raise_()
      
      first_list = [
        account_username,
        buttons_frame,
      ]
      for item in first_list:
        item.setParent(account_frame); account_frame.raise_()
        item.show()
        item.raise_()
      
      shadow.internal["config"]['account_widgets'].append(account_frame)
      shadow.internal["config"]['widget_values'][account_frame] = {
        "channel_id" : channel_id,
        "token" : token,
        "account_username" : account_username,
        "account_id" : account_id,
        "webhook_url" : webhook_url,
      }

      trash_button.clicked.connect(lambda: self.delete_account(trash_button))
      edit_button.clicked.connect(lambda: self.editing_account_popup(edit_button))
      settings_button.clicked.connect(lambda: self.show_alt_window(shadow.internal["config"]['widget_values'][account_frame]["account_id"]))
      globalize_settings_button.clicked.connect(lambda: self.globalize_settings(globalize_settings_button))
      view_logs_button.clicked.connect(lambda: self.show_account_logs(account_id))

      create_account_file(account_id)
      data = get_account_settings(account_id)
      data["data"]["token"] = str(token)
      data["data"]["channel_id"] = int(channel_id)
      data["data"]["account_id"] = int(account_id)
      data["data"]["webhook_url"] = str(webhook_url)
      update_account_settings(account_id, data)
      ensure_new_keys_get_added(account_id)

    @asyncSlot()
    async def editing_info_process(self):
      from utils.info import validate_token, validate_channel, validate_hook
      from utils.notifs import critical_messagebox, notification_messagebox
      import base64
      channel_id = self.editing_channel_id_input.text() # must stay here because it will be resetted later
      token = self.editing_token_input.text() # must stay here because it will be resetted later
      webhook_url = self.editing_webhook_url_input.text() # must stay here because it will be resetted later

      if len(token) == 0:#continue from here 
        return  critical_messagebox(shadow.internal["config"]["tray_icon"], "Token not supplied", "You haven't added a token.")
      if len(channel_id) == 0:#continue from here 
        return  critical_messagebox(shadow.internal["config"]["tray_icon"], "Channel ID not supplied", "You haven't added a channel ID.")
      
      self._popups_frame.setGeometry(QtCore.QRect(180, 50, 501, 311))
      self.editing_validating_popup.setGeometry(QtCore.QRect(0, 0, 501, 311))
      self.editing_validating_popup.show()

      validation_state, username, account_id = await validate_token(token)
      channel_state = await validate_channel(token, channel_id)
      if len(webhook_url) > 0 and validation_state is True:
        webhook_state = await validate_hook(token, webhook_url)

      self._popups_frame.setGeometry(QtCore.QRect(1800, 50, 501, 311))
      self.editing_validating_popup.setGeometry(QtCore.QRect(1000, 0, 501, 311))
      self.editing_validating_popup.hide()
      
      if validation_state is False:
        self.editing_webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_token_input.setStyleSheet("border: 2px solid red;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
        return critical_messagebox(shadow.internal["config"]["tray_icon"], "Invalid Token", f"The token you've added is invalid.")
      
      if channel_state is False:
        self.editing_token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_channel_id_input.setStyleSheet("border: 2px solid red;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
        return critical_messagebox(shadow.internal["config"]["tray_icon"], "Invalid Channel", f"The channel ID you've added is invalid.")
      
      if len(webhook_url) > 0 and validation_state is True and webhook_state is False:
        self.editing_token_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
        self.editing_webhook_url_input.setStyleSheet("border: 2px solid red;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
        return critical_messagebox(shadow.internal["config"]["tray_icon"], "Invalid Webhook URL", f"The Webhook URL you've added is invalid.")

      if len(webhook_url) > 0 and webhook_state is True:
        shadow.internal["config"]['previous_webhook_url'] = webhook_url

      self.editing_token_input.setStyleSheet("border: 2px solid green;\nborder-radius: 10px;\ncolor: white;\npadding-left:5px;")
      self.editing_channel_id_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.editing_webhook_url_input.setStyleSheet("border: 2px solid rgb(39,65,100); border-radius: 10px; color: white; padding-left:5px;")
      self.close_token_popup()

      father = shadow.internal["config"]['previous_father']
      for widget in shadow.internal["config"]['account_widgets']:
        if widget != father:
          if shadow.internal["config"]['widget_values'][widget]["token"].replace('\n', '') == token.replace('\n', ''):
            return  critical_messagebox(shadow.internal["config"]["tray_icon"], "Token already added", f"There is already an account that has this token.")

      father_data = shadow.internal["config"]['widget_values'][father]
      father_data["token"] = token
      father_data["channel_id"] = channel_id
      father_data["account_id"] = account_id
      father_data["webhook_url"] = webhook_url
      # father_data["account_username"].setText(new_username_text(username))

      data = get_account_settings(account_id)
      data["data"]["token"] = str(token)
      data["data"]["channel_id"] = int(channel_id)
      data["data"]["account_id"] = int(account_id)
      data["data"]["webhook_url"] = str(webhook_url)
      update_account_settings(account_id, data)
      return  critical_messagebox(shadow.internal["config"]["tray_icon"], "Data updated", f"The data of the account \"{username}\" has been updated.")

    def run_or_pause(self):
      
      from utils.notifs import notification_messagebox
      # from utils.alt_handler_assist import get_account_settings, update_account_settings
      import os

      appdata = os.getenv('APPDATA')
      directory = f"{appdata}\\Darkend v1"
      alt_handler_directory = f"{directory}\\Darkend Alt Handler"

      if shadow.internal["config"]['bots_running'] is None:
        self.run_accounts()
        # No data changing here because of a check inside that function
      elif shadow.internal["config"]['bots_running'] is True:
        # data_recieved = get_account_settings(file.split('.')[0])
        # account_id = data_recieved["data"]["account_id"]

        for account_id in messenger.internal:
          messenger.internal[account_id]['autofarming'] = False
        
        shadow.internal["config"]['bots_running'] = False
        self.run_accounts_button.setText("RESUME AUTOFARMING")
        notification_messagebox(shadow.internal["config"]["tray_icon"], "Autofarming has been paused", "All accounts have stopped autofarming now.")
      else:
        for account_id in messenger.internal:
          messenger.internal[account_id]['autofarming'] = True
        shadow.internal["config"]['bots_running'] = True
        self.run_accounts_button.setText("PAUSE AUTOFARMING")
        notification_messagebox(shadow.internal["config"]["tray_icon"], "Autofarming has been resumed", "All accounts have resumed autofarming now.")

    @asyncSlot()
    async def run_accounts(self):
      from utils.notifs import critical_messagebox_multi_gui, notification_messagebox_multi_gui
      
      from utils.multiple_bots import start_bots, between_callback
      from threading import Thread
      import asyncio

      tokens = []
      accounts = {}
      tokens_amount = len(shadow.internal["config"]['account_widgets'])

      if tokens_amount == 0:
        return critical_messagebox_multi_gui(shadow.internal["config"]["tray_icon"], "No accounts added", "You need to add at least 1 account in order to run the bots.")

      self.run_accounts_button.setText("PAUSE AUTOFARMING")
      shadow.internal["config"]['bots_running'] = True

      for widget in shadow.internal["config"]['account_widgets']:
        token = shadow.internal["config"]['widget_values'][widget]["token"].replace('\n', '')
        webhook_url = shadow.internal["config"]['widget_values'][widget]["webhook_url"].replace('\n', '')
        account_id = int(shadow.internal["config"]['widget_values'][widget]["account_id"])
        channel_id = int(shadow.internal["config"]['widget_values'][widget]["channel_id"])
        accounts[token] = {"account_id": account_id, "channel_id": channel_id, "webhook_url": webhook_url}

      # for token in tokens:
      for key, value in accounts.items():
        t1 = Thread(target = between_callback, args = [key, value["account_id"], shadow.internal["config"]["tray_icon"], messenger])
        t1.daemon = True
        t1.start()
        if len(accounts) > 1:
          await asyncio.sleep(0.5)
      
      notification_messagebox_multi_gui(shadow.internal['config']['tray_icon'], "Starting autofarm", "Accounts will start autofarming now.")

    def retranslateUi(self, MultipleAccounts):
      _translate = QtCore.QCoreApplication.translate
      MultipleAccounts.setWindowTitle(_translate("MultipleAccounts", "Darkend - Dank Memer Autofarm By Sxvxge"))
      self.add_account_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Checking pre-saved accounts...</span></p></body></html>"))
      self.add_account_emoji.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:64px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:48px; font-weight:600;\">🡓</span></p></body></html>"))
      self.add_account_button.setText(_translate("MultipleAccounts", "ADD ACCOUNT"))
      self.run_accounts_button.setText(_translate("MultipleAccounts", "RUN ACCOUNTS"))
      self.load_tokens_popup_button.setText(_translate("MultipleAccounts", "LOAD TOKENS"))
      self.delete_accounts_button.setText(_translate("MultipleAccounts", "DELETE ACCOUNTS"))
      self.channel_id_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px; font-weight:600;\">Channel ID</span></p></body></html>"))
      self.token_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px; font-weight:600;\">Token</span></p></body></html>"))
      self.add_token.setText(_translate("MultipleAccounts", "ADD"))
      self.close_popup.setText(_translate("MultipleAccounts", "CLOSE"))
      self.validating_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Validating data...</span></p></body></html>"))
      self.coming_soon_title.setText(_translate("MultipleAccounts", "<html><head/><body><p align=\"center\"><span style=\" font-size:31px; font-weight:600;\">This Feature is Coming Soon!</span></p></body></html>"))
      self.coming_soon_close_button.setText(_translate("MultipleAccounts", "Close"))
      self.webhook_url_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px; font-weight:600;\">Webhook URL</span></p></body></html>"))

      self.editing_channel_id_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px; font-weight:600;\">Channel ID</span></p></body></html>"))
      self.editing_token_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px; font-weight:600;\">Token</span></p></body></html>"))
      self.editing_token.setText(_translate("MultipleAccounts", "EDIT"))
      self.editing_close_popup.setText(_translate("MultipleAccounts", "CLOSE"))
      self.editing_webhook_url_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px; font-weight:600;\">Webhook URL</span></p></body></html>"))
      self.editing_validating_title.setText(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Century Gothic\'; font-size:43px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Validating data...</span></p></body></html>"))

      self.mass_tokens_input.setToolTip(_translate("MultipleAccounts", "<html><head/><body><p align=\"center\">Each token is separated by a line, only valid tokens will be shown in the GUI.</p></body></html>"))
      self.mass_tokens_input.setHtml(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Cascadia Mono\'; font-size:11px; font-weight:400; font-style:normal;\">\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:13px;\"><br /></p></body></html>"))
      self.format_text.setText(_translate("MultipleAccounts", "<html><head/><body><p align=\"center\"><span style=\" font-size:13px; font-weight:600; color:#ffffff;\">FORMAT: </span><span style=\" font-size:13px; color:#ffffff;\">Token:ChannelID:WebhookURL || Webhook URL is optional.</span></p></body></html>"))
      self.default_channel_label.setHtml(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Cascadia Mono\'; font-size:11px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px;\">Default channel ID</span></p></body></html>"))
      self.default_webhook_label.setHtml(_translate("MultipleAccounts", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'Cascadia Mono\'; font-size:11px; font-weight:400; font-style:normal;\">\n<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13px;\">Default webhook URL</span></p></body></html>"))
      self.default_webhook_input.setToolTip(_translate("MultipleAccounts", "<html><head/><body><p align=\"center\">Webhook URL is optional.</p></body></html>"))
      self.close_tokens_popup.setText(_translate("MultipleAccounts", "CLOSE"))
      self.load_tokens_button.setText(_translate("MultipleAccounts", "LOAD"))

if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  MultipleAccounts = QtWidgets.QMainWindow()
  ui = Ui_MultipleAccounts()
  ui.setupUi(MultipleAccounts)
  MultipleAccounts.show()
  sys.exit(app.exec_())