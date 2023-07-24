from PyQt5.QtWidgets import QApplication, QTableView, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QFont
import pandas as pd
import sys
import os
import pickle

class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, (Qt.DisplayRole, ))
            return True
        return False

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def flags(self, index):
        original_flags = super(TableModel, self).flags(index)
        return original_flags | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def addRow(self):
        self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex()))
        self._data = self._data.append(pd.Series(['', '', '', ''], index=self._data.columns), ignore_index=True)
        self.endInsertRows()

    def saveData(self):
        path, _ = QFileDialog.getSaveFileName()
        if path:
            with open(path, 'wb') as stream:
                pickle.dump(self._data, stream)

    def loadData(self):
        path, _ = QFileDialog.getOpenFileName()
        if path:
            with open(path, 'rb') as stream:
                self._data = pickle.load(stream)
                self.layoutChanged.emit()

def main():
    app = QApplication(sys.argv)

    data = pd.DataFrame(columns=['#', 'Title', 'Content', 'Keywords'])
    data.loc[0] = ['1', 'Template', 'Template', 'Template']

    view = QTableView()
    model = TableModel(data)
    view.setModel(model)

    addRowButton = QPushButton("Add Row")
    addRowButton.clicked.connect(model.addRow)

    saveButton = QPushButton("Save")
    saveButton.clicked.connect(model.saveData)

    loadButton = QPushButton("Load")
    loadButton.clicked.connect(model.loadData)

    layout = QVBoxLayout()
    layout.addWidget(view)
    layout.addWidget(addRowButton)
    layout.addWidget(saveButton)
    layout.addWidget(loadButton)

    widget = QWidget()
    widget.setLayout(layout)
    widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

