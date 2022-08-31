import sys

from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QWidget,
    QPushButton
)

class ShowButton(QAction):    
    def __init__(self, parent):
        super(ShowButton, self).__init__("Show", parent)     
    
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        pass          


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


class ExitButton(QWidget):
    def __init__(self):
        super().__init__()
        self.default_text = "Exit"
        self.btn = QPushButton(self.default_text, self)
        
    def on_click(self):
        sys.exit() 
    