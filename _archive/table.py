from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QListWidget
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['#', 'Title', 'Content', 'Keywords'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.setCentralWidget(self.table)

        self.keywords_list = QListWidget(self)
        self.keywords_list.itemClicked.connect(self.add_keyword)
        self.keywords_list.move(600, 0)

        self.data = {
            '#': ['1', '2', '3'],
            'Title': ['Title1', 'Title2', 'Title3'],
            'Content': ['Content1', 'Content2', 'Content3'],
            'Keywords': ['keyword1, keyword2', 'keyword3, keyword2', 'keyword1, keyword3'],
        }

        self.keywords = set(', '.join(self.data['Keywords']).split(', '))

        self.fill_table()
        self.fill_keywords()

    def fill_table(self):
        for i in range(len(self.data['#'])):
            self.table.insertRow(i)
            for j, key in enumerate(self.data.keys()):
                self.table.setItem(i, j, QTableWidgetItem(self.data[key][i]))

    def fill_keywords(self):
        for keyword in self.keywords:
            self.keywords_list.addItem(keyword)

    def add_keyword(self, item):
        current_row = self.table.currentRow()
        if current_row != -1:
            current_item = self.table.item(current_row, 3)
            current_item.setText(current_item.text() + ', ' + item.text())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
#

