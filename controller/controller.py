from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from model.model import WGbotModel
from controller.adbconnecter import AdbConnecter
from controller.workerthread import WorkerThread
from controller.wsengine import WSEngine
import time

class WGbotCtrler(QObject):
	onLogCreated = pyqtSignal(str)
	"""docstring for WGbotCtrler"""
	def __init__(self, model: WGbotModel):
		super(QObject, self).__init__()
		self.model = model
		self.log = []

		self.adbconnecter = AdbConnecter()
		self.engine = WSEngine(self.model, self.adbconnecter)

		self.adbconnecter.logEvent.connect(self.logCreated)
		self.engine.logEvent.connect(self.logCreated)

	def startFarming(self):
		self.adbconnecter.startMonitoring()
		self.engine.startGame()

	def logCreated(self, logstring: str):
		self.onLogCreated.emit(logstring)

	def stopFarming(self):
		# Stop adb connection monitoring
		self.adbconnecter.exitConnecter()
		self.engine.exitEngine()

		

