import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget,
                             QMainWindow, QAction, qApp, QMenu, QTextEdit, QFileDialog)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import QCoreApplication


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(600, 400)
        self.center()

        self.setWindowTitle('LFNL TECH')
        self.setWindowIcon(QIcon('Icon.jpg'))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
