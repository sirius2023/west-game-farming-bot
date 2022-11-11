import os
import enum
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QStringListModel

class WGbotModel(QStringListModel):
	connectionStateChanged = pyqtSignal(bool)
	checkConnectionStateChanged = pyqtSignal(bool)
	"""docstring for WGbotModel"""
	def __init__(self):
		super(QStringListModel, self).__init__()
		self.account_list = [x for x in os.listdir(os.path.dirname(__file__) + '\\..\\conf')]
		self.actionList = []
		self.setStringList(self.account_list)

