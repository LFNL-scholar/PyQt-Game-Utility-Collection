import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget,
                             QMainWindow, QAction, qApp, QMenu)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import QCoreApplication

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 字体
        QToolTip.setFont(QFont('Rajdhani', 10))
        font = QFont('Rajdhani', 10)

        self.setToolTip('This is a <b>Qwidget</b> widget')

        # 按钮
        btn = QPushButton('Button', self)
        btn.setFont(font)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        # 退出按钮
        qbtn = QPushButton('Quit', self)
        qbtn.setFont(font)
        qbtn.clicked.connect(QCoreApplication.instance().quit)

        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 100)

        # 状态栏
        self.statusBar().showMessage('Ready')

        # 菜单栏
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAct)

        # 子菜单
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)

        newAct = QAction('New', self)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)

        # 勾选菜单
        self.statusbar = self.statusBar()
        # self.statusbar.showMessage('Ready')

        # menubar = self.menuBar() # 重复第48行
        viewMenu = menubar.addMenu('View')

        viewStatAct = QAction('View statusbar', self, checkable = True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)

        viewMenu.addAction(viewStatAct)

        # 界面大小
        # self.setGeometry(300, 300, 300, 220)
        self.resize(300, 220)
        self.center()

        self.setWindowTitle('LFNL TECH')
        self.setWindowIcon(QIcon('Icon.jpg'))

        self.show()

    # 关闭窗口提示
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 窗口中央显示
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 状态显示
    def toggleMenu(self, state):

        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    # 右键菜单
    def contextMenuEvent(self, event):

        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

