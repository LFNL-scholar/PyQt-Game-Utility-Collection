"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：
"""
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget
from PyQt5 import uic

class MainWindow(QMainWindow):  # 步骤1: 登录成功后的窗口类
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        uic.loadUi('UI/LogCataWin.ui', self)
        self.SearchButton.clicked.connect(self.ToPurchase)


        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        self.show()

    def ToPurchase(self):
        self.purchase = Purchase()  # 步骤4: 实例化新窗口
        self.purchase.show()  # 步骤5: 显示新窗口
        self.close()  # 关闭登录窗口

class Purchase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Purchase.ui', self)
        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        self.show()

    # 关闭窗口提示
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()