from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QMainWindow, QStackedWidget, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize
import pandas
from random import randrange
from timeit import default_timer as timer


INTERVAL = 3
SOURCE_FILE = 'Experiment.xlsx'
RESULTS_FILE = 'Results.xlsx'
STANDARD_SHEET = 'Standard menu'
CUSTOMIZED_SHEET = 'Customized menu'
RESULTS_SHEET = 'Results'


class ChangeableMenu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.stacked = QStackedWidget()
        self.mainLayerView = MainLayer(self.main_layer_event)
        self.standardMenuLayerView = StandardMenuLayer(self.found_button_event)
        self.customizedMenuLayerView = CustomizedMenuLayer(self.found_button_event)
        self.currentLayer = None
        self.targetItem = None
        self.startTime = self.endTime = self.time_total = 0
        self.count = 0

        self.init_ui()
        self.show()

    def init_ui(self):
        self.setMinimumSize(QSize(700, 500))

        self.setCentralWidget(self.stacked)
        self.stacked.addWidget(self.mainLayerView)
        self.stacked.addWidget(self.standardMenuLayerView)
        self.stacked.addWidget(self.customizedMenuLayerView)

    def main_layer_event(self):
        senderText = self.sender().text()
        if senderText == 'Standard Menu':
            self.stacked.setCurrentWidget(self.standardMenuLayerView)
            self.targetItem = self.standardMenuLayerView.targetItem
        elif senderText == 'Customized Menu':
            self.stacked.setCurrentWidget(self.customizedMenuLayerView)
            self.targetItem = self.customizedMenuLayerView.targetItem

        self.currentLayer = senderText
        self.startTime = timer()

    def found_button_event(self):
        senderText = self.sender().currentItem().text()
        if senderText == self.targetItem:
            self.endTime = timer()
            self.time_total = round(self.endTime - self.startTime, 1)
            self.count = self.time_total // INTERVAL + 1

            result_layer = ResultLayer(self.targetItem, self.time_total)
            self.stacked.addWidget(result_layer)
            self.stacked.setCurrentWidget(result_layer)
            self.record_results()

    def record_results(self):
        df_existing = pandas.read_excel(RESULTS_FILE, sheet_name=RESULTS_SHEET)
        writer = pandas.ExcelWriter(RESULTS_FILE)
        rows_existing = df_existing.shape[0]
        if rows_existing > 0:
            df_existing = df_existing.append({'Menu': self.currentLayer,
                                              'Target': self.targetItem,
                                              'Time': self.time_total,
                                              'Count': self.count}, ignore_index=True)
            df_existing.to_excel(writer, sheet_name=RESULTS_SHEET)
        else:
            df_init = pandas.DataFrame(columns=['Menu', 'Target', 'Time', 'Count'])
            df_init = df_init.append({'Menu': self.currentLayer,
                                      'Target': self.targetItem,
                                      'Time': self.time_total,
                                      'Count': self.count}, ignore_index=True)
            df_init.to_excel(writer, sheet_name=RESULTS_SHEET)

        writer.save()

class MainLayer(QWidget):

    def __init__(self, event):
        super(MainLayer, self).__init__()
        self.title = "Main Menu"
        self.init_elements(event)

    def init_elements(self, event):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout()
        button1 = QPushButton('Standard Menu')
        button2 = QPushButton('Customized Menu')
        button1.clicked.connect(event)
        button2.clicked.connect(event)
        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)


class MenuLayer(QWidget):
    def __init__(self):
        super(MenuLayer, self).__init__()

        self.columnSize = 0
        self.rowSize = 0
        self.targetItem = ""

    def init_elements(self, event, sheet):
        layout = QVBoxLayout()
        myTable = QTableWidget()

        df = pandas.read_excel(SOURCE_FILE, sheet_name=sheet)
        titles = [i for i in df.columns]
        self.columnSize = df.shape[1]
        self.rowSize = df.shape[0]+1
        myTable.setColumnCount(self.columnSize)
        myTable.setRowCount(self.rowSize)
        for column, title in enumerate(titles):
            item = QTableWidgetItem(title)
            myTable.setItem(0, column, item)
            for row, value in enumerate(df[title]):
                item = QTableWidgetItem(value)
                myTable.setItem(row+1, column, item)

        myTable.itemClicked.connect(event)

        x, y = self.random_coordinates()
        self.targetItem = df[titles[x]][y]
        helpLabel = QLabel(f"Please find the label: {self.targetItem}")
        helpLabel.setStyleSheet('color: red')

        layout.addWidget(helpLabel)
        layout.addWidget(myTable)
        self.setLayout(layout)

    def random_coordinates(self):
        return randrange(0, self.columnSize), randrange(1, self.rowSize)


class StandardMenuLayer(MenuLayer):

    def __init__(self, event):
        super(StandardMenuLayer, self).__init__()
        self.init_elements(event, sheet=STANDARD_SHEET)


class CustomizedMenuLayer(MenuLayer):

    def __init__(self, event):
        super(CustomizedMenuLayer, self).__init__()
        self.init_elements(event, sheet=CUSTOMIZED_SHEET)


class ResultLayer(QWidget):

    def __init__(self, target, time):
        super(ResultLayer, self).__init__()
        self.target = target
        self.time = time
        self.init_elements()

    def init_elements(self):
        layout = QVBoxLayout()
        label = QLabel(f"Congratulations! It took you {self.time}s to find the target \'{self.target}\'")

        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = ChangeableMenu()
    app.exec_()