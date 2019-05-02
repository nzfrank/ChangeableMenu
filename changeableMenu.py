from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QMainWindow, QStackedWidget, QLabel
from PyQt5.QtCore import QSize

class ChangeableMenu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setMinimumSize(QSize(300, 200))
        self.firstLayerView = TheFirstLayer(self.main_menu_event)
        self.secondLayerView = TheSecondLayer(self.secondary_menu_event)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.stacked.addWidget(self.firstLayerView)
        self.stacked.addWidget(self.secondLayerView)

    def main_menu_event(self):
        sender = self.sender()
        self.stacked.setCurrentWidget(self.secondLayerView)
        # if sender.text() == 'Top':
        #     self.stacked.setCurrentWidget(self.secondLayerView)
        # elif sender.text() == 'First':
        #     self.stacked.setCurrentWidget(self.firstLayerView)

    def secondary_menu_event(self):
        sender = self.sender()
        self.stacked.setCurrentWidget(self.firstLayerView)


class TheFirstLayer(QWidget):

    def __init__(self, event):
        super(TheFirstLayer, self).__init__()
        self.title = "Main Menu"
        self.init_elements(event)

    def init_elements(self, event):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout()
        label = QLabel('Main Menu')
        button1 = QPushButton('Top')
        button2 = QPushButton('Bottom')
        button1.clicked.connect(event)
        button2.clicked.connect(event)
        button1.move(130, 60)
        button1.resize(50,50)
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)


class TheSecondLayer(QWidget):
    def __init__(self, event):
        super(TheSecondLayer, self).__init__()
        self.init_elements(event)

    def init_elements(self, event):
        layout = QVBoxLayout()
        label = QLabel('Secondary Menu')
        button1 = QPushButton('First')
        button2 = QPushButton('Second')
        button1.clicked.connect(event)
        button2.clicked.connect(event)
        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = ChangeableMenu()
    app.exec_()