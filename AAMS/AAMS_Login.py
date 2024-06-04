"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：管理界面与功能实现
"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget, QDialog
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect

from AAMS_Main import MainWindow

from SQLs import *
from Airline_Union_db import *
import Config as C

# 导入界面所需图片
from AAMS.UI import images_rc

# 注册页面
class RegisterPage(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('UI/Sign.ui', self)
        self.setWindowIcon(QIcon('Images/Icon.jpg'))

        self.RegisterButton.clicked.connect(self.Register)

    def Register(self):
        account = self.lineEdit_Raccount.text()
        password = self.lineEdit_Rpassword.text()
        confirm_password = self.lineEdit_RconfirmPassword.text()

        # 验证账号和密码不能为空
        if not account or not password:
            QMessageBox.information(self, '错误', '账号和密码不能为空')
            return

        if password != confirm_password:
            QMessageBox.information(self, '错误', '密码和确认密码不一致')
            return

        # 在此添加其他注册逻辑，例如将账号和密码保存到数据库
        QMessageBox.information(self, '成功', '注册成功')
        self.close()

class LoginPage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Login.ui', self)
        self.setWindowIcon(QIcon('Images/Icon.jpg'))

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 消除周边的框框
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置阴影

        # 设置跳转
        # self.LoginButton.connect(lambda: self.stackedWidget_2.setCurrentIndex((0)))  # 登录界面
        # self.pushButton_Register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex((1)))  # 注册界面

        # 确定按钮设置
        self.LoginButton.clicked.connect(self.Login)
        self.SignButton.clicked.connect(self.OpenRegisterPage)

        self.show()

    # 登录函数
    def Login(self):
        if self.Ticket_User_Button.isChecked():

            if (self.lineEditUserName.text() == C.USER_USERNAME and
                    self.lineEditPassword.text() == C.USER_PASSWORD):

                self.mainWindow = MainWindow()  # 步骤4: 实例化新窗口
                self.mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')


        elif self.Airline_User_Button.isChecked():

            if (self.lineEditUserName.text() == C.AIRLINE_USERNAME and
                    self.lineEditPassword.text() == C.AIRLINE_PASSWORD):

                self.mainWindow = MainWindow()  # 步骤4: 实例化新窗口
                self.mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')

        elif self.Airport_User_Button.isChecked():

            if (self.lineEditUserName.text() == C.AIRPORT_USERNAME and
                    self.lineEditPassword.text() == C.AIRPORT_PASSWORD):

                self.mainWindow = MainWindow()  # 步骤4: 实例化新窗口
                self.mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')

        else:
            QMessageBox.information(self, '提示', '请选择您的身份')

    # 注册函数
    def OpenRegisterPage(self):
        self.registerPage = RegisterPage()
        self.registerPage.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginPage()
    sys.exit(app.exec_())
