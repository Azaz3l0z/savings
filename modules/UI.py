import sys

import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, 
    QPushButton,
    QDesktopWidget,
    QWidget,
    QGridLayout
)

from modules import money_manager
from modules.UI_modules.taskbar import *


def center(qwidget: QWidget):
    """_summary_

    Args:
        qwidget (QWidget): _description_
    """
    screen_size = QDesktopWidget().screenGeometry()
    window_size = qwidget.size()

    x = (screen_size.width() - window_size.width()) // 2
    y = (screen_size.height() - window_size.height()) // 2

    qwidget.move(x, y)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """_summary_

    Args:
        QMainWindow (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        
        # UI config
        scale_factor = 0.65
        screen_size = QDesktopWidget().screenGeometry()
        x, y = screen_size.width() * scale_factor, \
            screen_size.height() * scale_factor
        self.setWindowTitle("My App")
        self.setFixedSize(int(x), int(y))
        center(self)
        
        # Money Object
        self.moneyManager = money_manager.MoneyO('yago')
        
        # UI build
        self._createMenuBar()
        self._initUI()
        
    def _createMenuBar(self):
        # Creation and styling
        menuBar = self.menuBar()
        menuBar.setStyleSheet("background-color: #8D8282;")
        
        # Adding menu buttons using QAction
        menuBarDict = {
            "Import": ImportButton(self),
            "Show": ShowButton(self)
        }
        
        for key in menuBarDict:
            menuBar.addAction(menuBarDict[key])
    
    def _initUI(self):
        layout = QGridLayout()
        self.figure = plt.figure()
        self.grapher = money_manager.Grapher(self.figure, self.moneyManager)

        # Layout order
        
        btn_graph = QPushButton('Change plot')
        btn_pie = QPushButton('Change pie')
        
        btn_graph.clicked.connect(self.change_scatter)
        btn_pie.clicked.connect(self.change_pie)
        
        # layout.addWidget(self.grapher.basic_plot('food'), 0, 0, 1, 2)
        layout.addWidget(btn_graph, 1, 0)
        layout.addWidget(btn_pie, 1, 1)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def change_scatter(self):
        self.grapher.basic_plot('')
        
    def change_pie(self):
        self.grapher.pie_plot('food')
        
                

def run():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()