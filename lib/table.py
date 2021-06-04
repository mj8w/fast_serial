
from PyQt5.QtCore import QAbstractTableModel, Qt

# https://www.mfitzp.com/tutorials/qtableview-modelviews-numpy-pandas/

class ActionTableModel(QAbstractTableModel):

    def __init__(self, data):
        super(ActionTableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        _ = index
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        _ = index
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def setData(self, index, value):
        self._data[index.row()][index.column()] = value
        return True
