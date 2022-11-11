from PyQt5.QtCore import QObject, pyqtSignal
from controller.workerthread import WorkerThread
from model.model import WGbotModel
from controller.adbconnecter import AdbConnecter
from controller.screenoperator import ScreenOperator
from model.utils import loadJsonData, saveJsonData_oneIndent, saveJsonData_twoIndent, \
	readAllSizesFolders, buildDataFolder, getCoordFilePath
import time


class WSEngine(QObject):
	logEvent = pyqtSignal(str)
	"""docstring for WSengine"""
	buttonsfilename_ = "buttons.json"
	movements__filename_ = "movements.json"

	def __init__(self, model: WGbotModel, connecter: AdbConnecter):
		super(QObject, self).__init__()
		self.model_ = model
		self.connecter_ = connecter
		self.stopFlag_ = False

		self.width_, self.height_ = 1280, 720
		self.datPath_ = "C:/Users/NOX/Documents/work/westgame_bot/datas/{}x{}/coords/".format(
			self.width_, self.height_)

		self.screenoptr_ = ScreenOperator(self.connecter_, self.width_, self.height_)

		self.buttons_ = loadJsonData(self.datPath_ + self.buttonsfilename_)
		self.movements__ = loadJsonData(
			self.datPath_ + self.movements__filename_)
		self.genralconf_ = loadJsonData(
			"C:/Users/NOX/Documents/work/westgame_bot/conf/dh-75@hotmail.com/general.conf")

		self.thread_ = WorkerThread()

	def startGame(self):
		self.thread_.function = self.startEngine
		self.thread_.start()

	def exitEngine(self):
		self.stopFlag_ = True

	def startEngine(self):
		# Run the game first
		self.run_game()
		
		while True:
			if self.connecter_.connectedToDevice() == False:
				print("Stopping engine due to broken connection...")
				break

			# process general actions
			self.general_farming()


	def run_game(self):
		time.sleep(5)
		self.sendlog("Staring Game...")
		self.tap("start_ws")

		time.sleep(5)
		# wait for the game to start fully
		while self.screenoptr_.checkFrame("first_loading_screen"):
			self.sendlog("Initializing...")
			time.sleep(3)
		self.sendlog("Game started.")

		# close first pop up ad windows or calendar
		while self.screenoptr_.checkFrame("overal_scene") == False:
			if self.screenoptr_.checkFrame("event_calendar"):
				self.sendlog("Event Calendar appeared, close it...")
				self.tap("eventCal_close")
			if self.screenoptr_.checkFrame("start_ad_appear"):
				self.sendlog("Ad appears, close it...")
				self.tap("ad_close")
			if self.screenoptr_.checkFrame("first_popup_modal"):
				self.sendlog("New modal appeared, closing...")
				self.tap("ok")
		
		self.sendlog("Ready to start farming...")

	def general_farming(self):
		for action in self.genralconf_.keys():
			self.wait(5)
			if self.genralconf_[action] == 0:
				continue
			else:
				# {"Helps": 1, "TradingPost": 1, "SuperbChest": 1, "CollectMailRewards": 1, "DuelForGlory": 1,
				# "RecruitHeroes": 1, "CollectAdRewards": 1, "BattlepassRewards": 1, "ConvertTreasureMap": 1, 
				# "PlayPoker": 0, "ValorRewards": 0}
				# helps
				if action == "Helps":
					if self.screenoptr_.checkFrame("alliance_help"):
						self.sendlog("Detected: Helps")
						self.tap("help")
						self.wait(3)
						self.tap("help_helpall")
						self.sendlog("Success: Helps")

				if action == "CollectMailRewards":
					if self.screenoptr_.checkFrame("mail_bonus"):
						self.sendlog("Detected: Main Rewards")
						self.tap("mail")
						


	def sendlog(self, str):
		self.logEvent.emit(str)

	def swipe_points(self, start, stop, s):
		start = self.buttons_[start]
		stop = self.buttons_[stop]
		print("Swiping between %s and %s in %f" % (start, stop, s))
		self.connecter_.adb_swipe(
			[start[0] * self.width_, start[1] * self.height_, stop[2] * self.width_, stop[3] * self.height_], s)

	def swipe(self, name, s):
		if self.connecter_.connectedToDevice() == False:
			exit()
		coord = self.movements_[name]
		print("swiping according to the movement direction")
		# convert back from normalized values
		self.connecter_.adb_swipe(
			[coord[0][0] * self.width_, coord[0][1] * self.height_,
				coord[1][0] * self.width_, coord[1][1] * self.height_],
			s)

	def tap(self, name):
		if self.connecter_.connectedToDevice() == False:
			exit()

		# convert back from normalized values
		x, y = int(self.buttons_[
				   name][0] * self.width_,), int(self.buttons_[name][1] * self.height_)
		print("Tapping on %s at [%d, %d]" % (name, x, y))
		self.connecter_.adb_tap((x, y))

	def wait(self, s):
		decimal = s
		if int(s) > 0:
			decimal = s - int(s)
			for _ in range(int(s)):
				if self.connecter_.connectedToDevice() == False:
					exit()
				time.sleep(1)
		if self.connecter_.connectedToDevice() == False:
			exit()
		time.sleep(decimal)
