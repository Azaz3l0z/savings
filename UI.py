import sys

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
    QFileDialog
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

        self.setWindowTitle("My App")
        self.setFixedSize(500, 300)
        center(self)
        
        self._createMenuBar()
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        menuBarDict = {
            "Import": ImportButton(self)
        }
        
        for key in menuBarDict:
            menuBar.addAction(menuBarDict[key])
        

class ImportButton(QAction):    
    def __init__(self, parent):
        super(ImportButton, self).__init__("Import", parent)     
    
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Choose a File", "","All Files (*);;Python Files (*.py)")
        if fileName:
            print(fileName)

    
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