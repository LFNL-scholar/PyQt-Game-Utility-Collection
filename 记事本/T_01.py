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
        self.resize(600, 400)  # 调整窗口大小
        self.center()

        self.setWindowTitle('LFNL TECH')
        self.setWindowIcon(QIcon('Icon.jpg'))

        self.textEdit = QTextEdit(self)  # 添加 QTextEdit 小部件
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()

        self.show()

    def createActions(self):
        self.openAction = QAction(QIcon('open.png'), '打开', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('打开文件')
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QAction(QIcon('save.png'), '保存', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('保存文件')
        self.saveAction.triggered.connect(self.saveFile)

    def createMenus(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'r') as file:
                self.textEdit.setText(file.read())

    def saveFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
