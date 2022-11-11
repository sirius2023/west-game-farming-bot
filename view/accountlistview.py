from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QListView, QVBoxLayout, QLabel
from PyQt5.QtGui import *


class AccountListView(QListView):
	"""docstring for AccountListView"""
	def __init__(self):
		super(QListView, self).__init__()
		# # Example of adding a message directly 
		# # important: this will update the UI automatically
		# self.accountModel.addData('msg4')
		self.show()