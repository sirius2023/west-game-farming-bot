from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from model.model import WGbotModel
from controller.controller import WGbotCtrler
from view.setaccountswin import SetAccountWindow
import os
import time

class WGbotView(QWidget):
	"""docstring for WGbotView"""
	def __init__(self, model: WGbotModel, controller: WGbotCtrler):
		super(QWidget, self).__init__()

		self.model = model
		self.controller = controller

		self.setFixedWidth(450)
		self.setFixedHeight(500)

		# initialize layouts, create objects
		self.main_layout = QVBoxLayout()
		self.selectPart = QHBoxLayout()
		self.logPart = QVBoxLayout()
		self.buttonPart = QHBoxLayout()

		self.setAccounts = QPushButton("Accounts", self)
		self.setAccounts.adjustSize()

		self.logBox = QPlainTextEdit(self)
		self.logBox.setReadOnly(True)
		self.logBox.resize(1400, 300)

		self.btnStart = QPushButton("Start", self)
		self.btnStop = QPushButton("Stop", self)

		# initialize button slots
		self.setAccounts.clicked.connect(self.onSetAccount)
		self.btnStart.clicked.connect(self.onStart)
		self.btnStop.clicked.connect(self.onStop)

		self.btnStop.setEnabled(False)

		# initialize signals
		self.controller.onLogCreated.connect(self.logArrived)
		#self.model.engine.addLog.connect(self.logArrived)

	def setupUi(self, main_window: QMainWindow):
		main_window.setObjectName("controller_window")
		self.setObjectName("main_window")
		self.setStyleSheet("background-color: #e1e1e1")
		main_window.setStyleSheet("background-color: #e1e1e1")

		self.selectPart.addWidget(self.setAccounts, 3)
		self.selectPart.setSpacing(200);
		self.main_layout.addLayout(self.selectPart, 0)

		self.logPart.addWidget(self.logBox, 0)
		self.main_layout.addLayout(self.logPart, 1)

		self.buttonPart.addWidget(self.btnStart, 5)
		self.buttonPart.addWidget(self.btnStop, 6)
		self.main_layout.addLayout(self.buttonPart, 2)

		self.setLayout(self.main_layout)
		main_window.setCentralWidget(self)

	def onSetAccount(self):
		dlg = SetAccountWindow(self.model)
		dlg.exec()

	def onStart(self):
		self.btnStart.setEnabled(False)
		self.btnStop.setEnabled(True)
		self.controller.startFarming()

	def onStop(self):
		self.btnStart.setEnabled(True)
		self.btnStop.setEnabled(False)
		self.controller.stopFarming()

	def logArrived(self, log : str):
		self.logBox.appendPlainText(log)