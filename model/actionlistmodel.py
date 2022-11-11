import sys
import time

from PyQt5.QtCore import QAbstractListModel, pyqtSlot, QModelIndex, Qt

class ActionListModel(QAbstractListModel):
    def __init__(self):
        super(QAbstractListModel, self).__init__()
        self.action_list = ["Collect mail rewards",
                        "Collect alliance rewards",
                        "Transfer resources",
                        "Collect mail rewards"
                        "Collect elite daily gift",
                        "Collect Expedition daily gift",
                        "Collect alliance gifts (common and rare)",
                        "Collect superb chests gift",
                        "Collect valor challenges gift ",
                        "Collect civilians gifts",
                        "Collect west train gifts",
                        "Collect battel pass gifts",
                        "Collect growth quest",
                        "Collect Town quest",
                        "Collect Daily quest",
                        "Collect alliance quest",
                        "Collect VIP quest",
                        "Help button",
                        "Join gang of bandits",
                        "Join rally",
                        "Wild hunt attack",
                        "Gather rss from tiles",
                        "Use VIP chips",
                        "Use sheriff chips",
                        "Construction",
                        "Research",
                        "Convert resources",
                        "Transfer resources",
                        "Convert Treasure Maps",
                        "Auto Shielding",
                        "Troop Training",
                        "Duel for glory",
                        "Alliance carnival",
                        "Healing troops",
                        "Reviving troops",
                        "Watch ads to collect rewards"]

    def data(self, index, role=None):
        row = index.row()
        value = self.action_list[row]

        if role == Qt.DisplayRole:
            return value

    def rowCount(self, parent=None):
        return len(self.action_list)

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
            self.action_list[row] = value
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
        self.action_list.append(value)
        self.endInsertRows()
        print('I am adding the value: {} to my data store'.format(value))
        return True

    def getAccountList(self):
        return True
