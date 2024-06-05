"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：机场管理员主界面和功能的设计与实现
"""
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget, QPushButton, QStackedWidget
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QCoreApplication

from SQLs import *
from Airline_Union_db import *
import Config as C

# 全局变量

class Airport_MainWindow(QMainWindow):  # 步骤1: 登录成功后的窗口类
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Airport_User.ui', self)

        ## 获取控件
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.flight_searchButton = self.findChild(QPushButton, 'Flight_SearchButton')
        self.homeButton = self.findChild(QPushButton, 'HomeButton')
        self.orders_Button = self.findChild(QPushButton, 'Orders_Button')
        self.quit_Button = self.findChild(QPushButton, 'Quit_Button')

        # 设置初始页面为 Home
        self.stackedWidget.setCurrentIndex(0)

        # 连接按钮的点击事件到对应的方法
        self.flight_searchButton.clicked.connect(self.ToSearch)
        self.homeButton.clicked.connect(self.ToHome)
        self.orders_Button.clicked.connect(self.ToOrders)

        # 退出登录
        self.quit_Button.clicked.connect(QCoreApplication.instance().quit)


        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        self.show()

    # 主页面
    def ToHome(self):
        # 切换到主页面
        self.stackedWidget.setCurrentIndex(0)

    # 搜索航班界面
    def ToSearch(self):
        # 切换到搜索页面
        self.stackedWidget.setCurrentIndex(1)

    # 我的订单界面
    def ToOrders(self):
        # 切换到搜索页面
        self.stackedWidget.setCurrentIndex(2)

    # 关闭窗口提示
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    airport_mainWindow = Airport_MainWindow()
    sys.exit(app.exec_())
