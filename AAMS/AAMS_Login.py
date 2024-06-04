"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：管理界面与功能实现
"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget
from PyQt5 import uic
from PyQt5.QtGui import QIcon

from AAMS_Main import MainWindow
from AAMS import Config

from SQLs import *
from Airline_Union_db import *

# 导入界面所需图片
from AAMS.UI import images_rc

class LoginPage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Login.ui', self)
        self.LoginButton.clicked.connect(self.Login)

        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        self.show()

    # 登录函数
    def Login(self):
        if self.Ticket_User_Button.isChecked():

            if (self.lineEditUserName.text() == Config.USER_USERNAME and
                    self.lineEditPassword.text() == Config.USER_PASSWORD):

                self.mainWindow = MainWindow()  # 步骤4: 实例化新窗口
                self.mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')


        elif self.Airline_User_Button.isChecked():

            if (self.lineEditUserName.text() == Config.AIRLINE_USERNAME and
                    self.lineEditPassword.text() == Config.AIRLINE_PASSWORD):

                self.mainWindow = MainWindow()  # 步骤4: 实例化新窗口
                self.mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')

        elif self.Airport_User_Button.isChecked():

            if (self.lineEditUserName.text() == Config.AIRPORT_USERNAME and
                    self.lineEditPassword.text() == Config.AIRPORT_PASSWORD):

                self.mainWindow = MainWindow()  # 步骤4: 实例化新窗口
                self.mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')

        else:
            QMessageBox.information(self, '提示', '请选择您的身份')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginPage()
    sys.exit(app.exec_())
