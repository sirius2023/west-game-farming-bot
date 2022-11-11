from PyQt5 import QtWidgets, QtGui, QtCore
from model.model import WGbotModel
from view.view import WGbotView
from controller.controller import WGbotCtrler

if __name__ == "__main__":
    import sys

    # initialize the app
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(MainWindow.windowFlags() & QtCore.Qt.CustomizeWindowHint)
    MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
    MainWindow.setWindowTitle("West Game Farming Bot")
    MainWindow.setWindowIcon(QtGui.QIcon('resource/icon/icon.png'))

    # Model initialization
    model = WGbotModel()

    # Controller initialization
    controller = WGbotCtrler(model)

    # View initialization
    ui = WGbotView(model, controller)
    ui.setupUi(MainWindow)

    # model.load_data()
    
    MainWindow.show()
    result = app.exec_()
    sys.exit(result)
