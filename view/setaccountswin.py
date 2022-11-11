# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from view.accountlistview import AccountListView
from view.setactionswin import SetActionsWindow
from model.model import WGbotModel
import sys

class SetAccountWindow(QDialog):
	"""docstring for WGbotView"""
	def __init__(self, model: WGbotModel):
		super(QWidget, self).__init__()

		self.model = model
		self.setWindowTitle("Accounts")
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint);

		# initialize layouts, create objects
		self.comment = QLabel("Available Accounts", self)
		self.comment.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.comment.setAlignment(Qt.AlignCenter)

		self.main_layout = QVBoxLayout()
		self.commentPart = QVBoxLayout()
		self.accountListPart = QVBoxLayout()
		self.buttonPart = QHBoxLayout()

		self.okButton = QPushButton('OK')
		self.addButton = QPushButton('Add New')
		self.delButton = QPushButton('Delete')

		self.accountList = QListView()
		self.accountList.setModel(self.model)
		self.accountList.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked);
		self.accountList.doubleClicked.connect(self.onListItemMouseClick)

		self.buttonPart.addStretch(1)
		self.buttonPart.addWidget(self.okButton)
		self.buttonPart.addWidget(self.addButton)
		self.buttonPart.addWidget(self.delButton)

		self.commentPart.addWidget(self.comment, 0)
		self.accountListPart.addWidget(self.accountList, 0)

		self.main_layout.addLayout(self.commentPart, 0)
		self.main_layout.addLayout(self.accountListPart, 1)
		self.main_layout.addLayout(self.buttonPart, 2)

		self.setLayout(self.main_layout)

		# initialize button slots
		self.okButton.clicked.connect(self.accept)
		self.addButton.clicked.connect(self.addNew)
		self.delButton.clicked.connect(self.delete)

	def addNew(self):
		print('add new')

	def delete(self):
		print('delete')

	def onListItemMouseClick(self, index):
		dlg = SetActionsWindow(self.model, index.row())
		dlg.exec()
		self.close()

