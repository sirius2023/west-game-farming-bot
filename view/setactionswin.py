# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from model.model import WGbotModel
import sys
import os
import json

class SetActionsWindow(QDialog):
	"""docstring for WGbotView"""
	def __init__(self, model: WGbotModel, accountIndex):
		super(QWidget, self).__init__()

		self.model = model
		self.accountIndex = accountIndex
		self.setWindowTitle("Set Farming Actions")
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint);

		# initialize layouts, create objects

		# main layout
		self.main_layout = QVBoxLayout()

		# general
		self.general = QGroupBox("General", self)
		self.general_layout = QGridLayout()
		self.general.setLayout(self.general_layout)

		self.helps = QCheckBox("Helps", self)
		self.general_layout.addWidget(self.helps, 1, 0)

		self.mailRewards = QCheckBox("Collect Mail Rewards", self)
		self.general_layout.addWidget(self.mailRewards, 1, 1)

		self.adRewards = QCheckBox("Collect Ad Rewards", self)
		self.general_layout.addWidget(self.adRewards, 1, 2)

		self.playPoker = QCheckBox("Play Poker", self)
		self.general_layout.addWidget(self.playPoker, 1, 3)

		self.tradingPost = QCheckBox("Trading Post", self)
		self.general_layout.addWidget(self.tradingPost, 2, 0)

		self.duelforglory = QCheckBox("Duel for Glory", self)
		self.general_layout.addWidget(self.duelforglory, 2, 1)

		self.battlepassRewards = QCheckBox("Battlepass Rewards", self)
		self.general_layout.addWidget(self.battlepassRewards, 2, 2)

		self.valorRewards = QCheckBox("Valor Rewards", self)
		self.general_layout.addWidget(self.valorRewards, 2, 3)

		self.superbChest = QCheckBox("Superb Chest", self)
		self.general_layout.addWidget(self.superbChest, 3, 0)

		self.recruitHeroes = QCheckBox("Recruit Heroes", self)
		self.general_layout.addWidget(self.recruitHeroes, 3, 1)

		self.convertTreasureMap = QCheckBox("Convert Treasure Map", self)
		self.general_layout.addWidget(self.convertTreasureMap, 3, 2)

		# Resource management
		self.resMgmt = QGroupBox("Resource Management", self)
		self.resmgr_layout = QGridLayout()
		self.resMgmt.setLayout(self.resmgr_layout)

		self.convertCheck = QCheckBox("Convert", self)
		self.resmgr_layout.addWidget(self.convertCheck, 0, 0)

		self.convertLabel = QLabel("Select which resources to convert to", self)
		self.resmgr_layout.addWidget(self.convertLabel, 1, 0)

		self.grain = QCheckBox("Grain", self)
		self.resmgr_layout.addWidget(self.grain, 2, 0)

		self.log = QCheckBox("Logs", self)
		self.resmgr_layout.addWidget(self.log, 2, 1)

		self.rubbles = QCheckBox("Rubbles", self)
		self.resmgr_layout.addWidget(self.rubbles, 2, 2)

		self.iron = QCheckBox("Iron", self)
		self.resmgr_layout.addWidget(self.iron, 2, 3)

		self.silver = QCheckBox("Silver", self)
		self.resmgr_layout.addWidget(self.silver, 2, 4)

		self.corn = QCheckBox("Corn", self)
		self.resmgr_layout.addWidget(self.corn, 3, 0)

		self.rosewood = QCheckBox("Rosewood", self)
		self.resmgr_layout.addWidget(self.rosewood, 3, 1)

		self.rocks = QCheckBox("Rocks", self)
		self.resmgr_layout.addWidget(self.rocks, 3, 2)

		self.brass = QCheckBox("Brass", self)
		self.resmgr_layout.addWidget(self.brass, 3, 3)

		self.spanishCoin = QCheckBox("Spanish Coin", self)
		self.resmgr_layout.addWidget(self.spanishCoin, 3, 4)

		self.bankDepositCheck = QCheckBox("Bank Deposit", self)
		self.resmgr_layout.addWidget(self.bankDepositCheck, 4, 0)

		self.banknameLabel = QLabel("Bank Name", self)
		self.resmgr_layout.addWidget(self.banknameLabel, 5, 0)

		self.bankName = QTextEdit(self);
		self.resmgr_layout.addWidget(self.bankName, 6, 0)
		self.bankName.setFixedHeight(24)

		self.shippingPrefrnces = QLabel("Shipping Preferences", self)
		self.resmgr_layout.addWidget(self.shippingPrefrnces, 7, 0)

		self.grainShip = QCheckBox("Grain", self)
		self.resmgr_layout.addWidget(self.grainShip, 8, 0)

		self.logShip = QCheckBox("Logs", self)
		self.resmgr_layout.addWidget(self.logShip, 8, 1)

		self.rubblesShip = QCheckBox("Rubbles", self)
		self.resmgr_layout.addWidget(self.rubblesShip, 8, 2)

		self.ironShip = QCheckBox("Iron", self)
		self.resmgr_layout.addWidget(self.ironShip, 8, 3)

		self.silverShip = QCheckBox("Silver", self)
		self.resmgr_layout.addWidget(self.silverShip, 8, 4)

		self.cornShip = QCheckBox("Corn", self)
		self.resmgr_layout.addWidget(self.cornShip, 9, 0)

		self.rosewoodShip = QCheckBox("Rosewood", self)
		self.resmgr_layout.addWidget(self.rosewoodShip, 9, 1)

		self.rocksShip = QCheckBox("Rocks", self)
		self.resmgr_layout.addWidget(self.rocksShip, 9, 2)

		self.brassShip = QCheckBox("Brass", self)
		self.resmgr_layout.addWidget(self.brassShip, 9, 3)

		self.spanishCoinShip = QCheckBox("Spanish Coin", self)
		self.resmgr_layout.addWidget(self.spanishCoinShip, 9, 4)

		self.redeemChips = QCheckBox("Redeem Chips", self)
		self.resmgr_layout.addWidget(self.redeemChips, 10, 0)
		
		self.advance_layout = QGridLayout()
		self.gifts_layout = QGridLayout()
		self.tbasedboost_layout = QGridLayout()
		self.vip_layout = QGridLayout()
		self.hero_layout = QGridLayout()

		# button layout
		self.buttonPart = QHBoxLayout()
		
		self.okButton = QPushButton('OK')
		self.cancelButton = QPushButton('Cancel')

		self.buttonPart.addStretch(3)
		self.buttonPart.addWidget(self.okButton)
		self.buttonPart.addWidget(self.cancelButton)

		self.setObjectName("main_window")

		self.main_layout.addWidget(self.general, 0)
		self.main_layout.addWidget(self.resMgmt, 1)
		self.main_layout.addLayout(self.advance_layout, 2)
		self.main_layout.addLayout(self.gifts_layout, 3)
		self.main_layout.addLayout(self.tbasedboost_layout, 4)
		self.main_layout.addLayout(self.vip_layout, 5)
		self.main_layout.addLayout(self.hero_layout, 6)
		self.main_layout.addLayout(self.buttonPart, 7)

		self.setLayout(self.main_layout)

		# initialize button slots
		self.okButton.clicked.connect(self.onAccepted)
		self.cancelButton.clicked.connect(self.reject)

	def onAccepted(self):
		confPath = os.path.dirname(__file__) + '\\..\\conf\\' + self.model.account_list[self.accountIndex]

		# create general.conf
		generalConf = {
			"Helps" : 0,
			"TradingPost" : 0,
			"SuperbChest" : 0,
			"CollectMailRewards" : 0,
			"DuelForGlory" : 0,
			"RecruitHeroes" : 0,
			"CollectAdRewards" : 0,
			"BattlepassRewards" : 0,
			"ConvertTreasureMap" : 0,
			"PlayPoker" : 0,
			"ValorRewards" : 0
		}

		if self.helps.isChecked():
			generalConf["Helps"] = 1
		if self.tradingPost.isChecked():
			generalConf["TradingPost"] = 1
		if self.superbChest.isChecked():
			generalConf["SuperbChest"] = 1
		if self.mailRewards.isChecked():
			generalConf["CollectMailRewards"] = 1
		if self.duelforglory.isChecked():
			generalConf["DuelForGlory"] = 1
		if self.recruitHeroes.isChecked():
			generalConf["RecruitHeroes"] = 1
		if self.adRewards.isChecked():
			generalConf["CollectAdRewards"] = 1
		if self.battlepassRewards.isChecked():
			generalConf["BattlepassRewards"] = 1
		if self.convertTreasureMap.isChecked():
			generalConf["ConvertTreasureMap"] = 1
		if self.playPoker.isChecked():
			generalConf["PlayPoker"] = 1
		if self.valorRewards.isChecked():
			generalConf["ValorRewards"] = 1
		
		with open(confPath + '\\general.conf', "w") as outfile:
			json.dump(generalConf, outfile)

		self.accept()
