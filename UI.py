import sys
import file_manager

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, 
    QPushButton,
    QDesktopWidget,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMenu,
    QAction,
    QFileDialog,
    QGridLayout,
    QDialog
)

from PyQt5.QtGui import (
    QPalette, 
    QColor
)

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
        self.moneyManager = file_manager.MoneyO('yago')
        
        # UI build
        self._createMenuBar()
        self._initUI()
    
    def _createMenuBar(self):
        # Creation and styling
        menuBar = self.menuBar()
        menuBar.setStyleSheet("background-color: yellow;")
        
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
        self.canvas = FigureCanvas(self.figure)
        
        data = self.moneyManager.get_data()["amount"]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'ro')
        self.canvas.draw()

        # Layout order
        layout.addWidget(self.canvas, 0, 0, 1, 2)
        layout.addWidget(QPushButton("Gayass"), 1, 0)
        layout.addWidget(QPushButton("Gay2"), 1, 1)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
            

class ShowButton(QAction):    
    def __init__(self, parent):
        super(ShowButton, self).__init__("Show", parent)     
    
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        print(self.parent().moneyManager.get_data())            


class ImportButton(QAction):    
    def __init__(self, parent):
        super(ImportButton, self).__init__("Import", parent)     
    
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Choose a File", "",
                                                "Excel Files (*.xls *.xlsx);;" + \
                                                "CSV Files (*.csv)")
        if fileName:
            self.parent().moneyManager.add_data(fileName)
        print(self.parent().moneyManager.get_data())


class ExitButton(QWidget):
    def __init__(self):
        super().__init__()
        self.default_text = "Exit"
        self.btn = QPushButton(self.default_text, self)
        
    def on_click(self):
        sys.exit() 
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()