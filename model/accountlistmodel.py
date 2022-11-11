import sys
import time
import os
from copy import deepcopy

from PyQt5.QtCore import QAbstractListModel, pyqtSlot, QModelIndex, Qt

class AccountListModel(QAbstractListModel):
    def __init__(self):
        super(QAbstractListModel, self).__init__()
        # get added account list from config subdirectories
        self.account_list = [x for x in os.listdir(os.path.dirname(__file__) + '\\..\\conf')]

    def data(self, index, role=None):
        row = index.row()
        value = self.account_list[row]

        if role == Qt.DisplayRole:
            return value

    def rowCount(self, parent=None):
        return len(self.account_list)

    def flags(self, QModelIndex):
        # These items are editable so that we can edit each row
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    @pyqtSlot()
    def setData(self, QModelIndex, value, role=None):
        """
        To be used to modify an existing element in the list (e.g. the reply window)
        We can also leave this unimplemented.
        """
        if role == Qt.EditRole:
            row = QModelIndex.row()
            print('I am changing the value of row {} to be {} in my data store'.format(row, value))
            self.account_list[row] = value
            # Emit dataChanged and now just that row should be repainted
            # This is what we should do to resolve
            # https://github.com/freedomofpress/securedrop-client/issues/185
            self.dataChanged.emit(QModelIndex, QModelIndex, [])
            return True
        return False

    @pyqtSlot()
    def addData(self, value):
        """
        To be used when there's a new message in the conversation
        """
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.account_list.append(value)
        self.endInsertRows()
        print('I am adding the value: {} to my data store'.format(value))
        return True

    def getAccountList(self):
        # extract Nox installation path from PATH env variable
        # this is used to get the number of Nox instances
        pathList = os.getenv('Path').split(";")
        for proPath in pathList:
            if "Nox\\bin" in proPath:
                self.account_list = [x for x in os.listdir(proPath + "\\BignoxVMS")]
