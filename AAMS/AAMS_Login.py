"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：登录界面与功能实现
"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget, QDialog, QPushButton
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect

from AAMS.AAMS_AirLine_Main import Airline_MainWindow
from AAMS.AAMS_Airport_Main import Airport_MainWindow
from AAMS_User_Main import User_MainWindow

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
        # 获取信息
        account = self.lineEdit_Raccount.text()
        nick_name = self.lineEdit_NickName.text()
        real_name = self.lineEdit_RealName.text()
        phone_number = self.lineEdit_PhoneNumber.text()
        sex = self.lineEdit_Sex.text()
        csid = self.lineEdit_Sid.text()
        password = self.lineEdit_Rpassword.text()
        confirm_password = self.lineEdit_RconfirmPassword.text()

        # 验证基本信息不能为空
        if not nick_name or not real_name or not sex or not csid or not phone_number:
            QMessageBox.information(self, '错误', '基本信息不能为空')
            return

        # 验证账号和密码不能为空
        if not account or not password:
            QMessageBox.information(self, '错误', '账号和密码不能为空')
            return

        if password != confirm_password:
            QMessageBox.information(self, '错误', '密码和确认密码不一致')
            return

        # 将新购票用户信息插入数据库
        if create_user(account, nick_name, real_name, phone_number, csid, sex, password):
            QMessageBox.information(self, '成功', '注册成功')
            self.close()
        else:
            QMessageBox.information(self, '错误', '账号已存在')


class LoginPage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Login_M.ui', self)
        self.setWindowIcon(QIcon('Images/Icon.jpg'))

        # 退出按钮
        self.exit_btn.setToolTip('点击退出')  # 设置提示信息
        self.exit_btn.clicked.connect(self.close)  # 点击按钮关闭窗口

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 消除周边的框框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置阴影

        # 设置跳转
        # self.LoginButton.connect(lambda: self.stackedWidget_2.setCurrentIndex((0)))  # 登录界面
        # self.pushButton_Register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex((1)))  # 注册界面

        # 确定按钮设置
        self.LoginButton.clicked.connect(self.Login)
        self.SignButton.clicked.connect(self.OpenRegisterPage)

        self.show()

    # 登录函数
    def Login(self):

        # 购票用户判断逻辑
        account = self.lineEditUserName.text()
        password = self.lineEditPassword.text()

        if self.Ticket_User_Button.isChecked():

            if validate_user(account, password):
                    self.user_mainWindow = User_MainWindow(user_id = account)  # 步骤4: 实例化新窗口
                    self.user_mainWindow.show()  # 步骤5: 显示新窗口
                    self.close()  # 关闭登录窗口
                    # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')

        # 航司管理员判断逻辑
        elif self.Airline_User_Button.isChecked():

            if validate_flight_manager(account, password):

                self.airline_mainWindow = Airline_MainWindow()  # 步骤4: 实例化新窗口
                self.airline_mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')

        # 机场管理员判断逻辑
        elif self.Airport_User_Button.isChecked():

            if validate_Airport_manager(account, password):

                self.airport_mainWindow = Airport_MainWindow()  # 步骤4: 实例化新窗口
                self.airport_mainWindow.show()  # 步骤5: 显示新窗口
                self.close()  # 关闭登录窗口
                # 登录成功

            else:
                QMessageBox.information(self, '提示', '账号或密码输入错误')

        # 最外层选择身份判断逻辑
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
