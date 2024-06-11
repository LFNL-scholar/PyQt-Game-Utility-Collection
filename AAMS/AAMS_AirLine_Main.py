"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：航司管理员主界面和功能的设计与实现
"""
import os
import sys

import datetime

from datetime import datetime, timedelta
from wsgiref import headers

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget, QPushButton, \
    QStackedWidget, QLineEdit, QComboBox, QDateEdit, QVBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox, \
    QHBoxLayout, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QCoreApplication

from SQLs import *
from Airline_Union_db import *

import Config as C

# 导入界面所需图片
from AAMS.UI import images_rc

# 全局变量

class Airline_MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id  # 记录当前用户的ID

        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Airline_User.ui', self)

        ## 获取控件
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.homeButton = self.findChild(QPushButton, 'HomeButton')
        self.flight_searchButton = self.findChild(QPushButton, 'Flight_SearchButton')
        self.orders_Button = self.findChild(QPushButton, 'Orders_Button')
        self.quit_Button = self.findChild(QPushButton, 'Quit_Button')

        # 设置初始页面为 Home
        self.stackedWidget.setCurrentIndex(0)

        # 连接按钮的点击事件到对应的方法
        self.flight_searchButton.clicked.connect(self.ToPublish)
        self.homeButton.clicked.connect(self.ToHome)
        self.modifyButton.clicked.connect(self.ToModify)

        # 退出登录
        self.quit_Button.clicked.connect(QCoreApplication.instance().quit)


        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        self.show()

    # 主页面
    def ToHome(self):
        # 切换到主页面
        self.stackedWidget.setCurrentIndex(0)

    # 发布航班界面
    def ToPublish(self):
        # 切换到发布航班页面
        self.stackedWidget.setCurrentIndex(1)
        publish_page = self.stackedWidget.widget(1)

        publish_button = publish_page.findChild(QPushButton, 'PublishButton')

        publish_button.clicked.connect(self.Confirm)

    def Confirm(self):
        try:
            self.stackedWidget.setCurrentIndex(1)
            publish_page = self.stackedWidget.widget(1)

            # 获取各个 QLineEdit 对象
            flight_number_edit = publish_page.findChild(QLineEdit, 'FlightNumberEdit')
            plane_type_edit = publish_page.findChild(QLineEdit, 'PlaneTypeEdit')
            departure_city_edit = publish_page.findChild(QLineEdit, 'DepartureCityEdit')
            arrival_city_edit = publish_page.findChild(QLineEdit, 'ArrivalCityEdit')
            departure_airport_edit = publish_page.findChild(QLineEdit, 'DepartureAirportEdit')
            arrival_airport_edit = publish_page.findChild(QLineEdit, 'ArrivalAirportEdit')
            price_edit = publish_page.findChild(QLineEdit, 'PriceEdit')

            # 获取用户输入的数据
            flight_number = flight_number_edit.text()
            plane_type = plane_type_edit.text()
            departure_city = departure_city_edit.text()
            arrival_city = arrival_city_edit.text()
            departure_airport = departure_airport_edit.text()
            arrival_airport = arrival_airport_edit.text()
            price = price_edit.text()

            # 检查输入是否为空
            if not flight_number or not plane_type or not departure_city or not arrival_city \
                    or not departure_airport or not arrival_airport or not price:
                QMessageBox.warning(self, 'Error', '所有内容都是必填项，请填写完整信息。')
                return

            # 调用数据库插入函数
            if not publish_flight(flight_number, departure_city, arrival_city,
                                  departure_airport, arrival_airport, plane_type, price):
                raise Exception('发布航班信息失败，请重试。')
            QMessageBox.information(self, 'Success', '航班信息发布成功！')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'发生错误: {str(e)}')
            print(f'Exception: {str(e)}')


    # 修改资料界面
    def ToModify(self):
        try:
            # 切换到修改资料页面
            self.stackedWidget.setCurrentIndex(2)
            modify_page = self.stackedWidget.widget(2)

            self.realname_edit = modify_page.findChild(QLineEdit, 'realnameEdit')
            self.fsex_edit = modify_page.findChild(QLineEdit, 'fsexEdit')
            self.fmid_edit = modify_page.findChild(QLineEdit, 'fmidEdit')
            self.new_password_edit = modify_page.findChild(QLineEdit, 'newPasswordEdit')
            self.confirm_password_edit = modify_page.findChild(QLineEdit, 'confirmPasswordEdit')

            # 添加修改和确定按钮
            self.edit_button = modify_page.findChild(QPushButton, 'editButton')
            self.save_button = modify_page.findChild(QPushButton, 'saveButton')
            self.cancel_button = modify_page.findChild(QPushButton, 'cancelButton')

            # 初始化文本框为不可编辑状态
            self.set_text_fields_editable(False)

            # 加载用户信息
            self.load_user_info(self.user_id)

            # 连接按钮的点击事件到对应的方法
            self.edit_button.clicked.connect(self.enable_editing)
            self.save_button.clicked.connect(self.save_user_info)
            self.cancel_button.clicked.connect(self.cancel_editing)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'加载修改资料页面失败: {str(e)}')

    def set_text_fields_editable(self, editable):
        try:
            self.fmid_edit.setReadOnly(not editable)
            self.realname_edit.setReadOnly(not editable)
            self.fsex_edit.setReadOnly(not editable)
            self.new_password_edit.setReadOnly(not editable)
            self.confirm_password_edit.setReadOnly(not editable)
        except AttributeError as e:
            QMessageBox.warning(self, 'Error', f'设置文本框状态失败: {str(e)}')

    def enable_editing(self):
        try:
            self.set_text_fields_editable(True)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'启用编辑模式失败: {str(e)}')

    def load_user_info(self, fmid):
        try:
            user_info = get_airline_info(fmid)
            if not user_info:
                raise ValueError("未找到用户信息")

            self.realname_edit.setText(user_info[0])
            self.fsex_edit.setText(user_info[1])
            self.fmid_edit.setText(user_info[2])
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'加载用户信息失败: {str(e)}')

    def save_user_info(self):
        try:
            updated_info = {
                'FMID': self.fmid_edit.text(),
                'Fname': self.realname_edit.text(),
                'Fsex': self.fsex_edit.text(),
                'NewPassword': self.new_password_edit.text(),  # 新密码
                'ConfirmPassword': self.confirm_password_edit.text()  # 确认密码
            }

            if updated_info['NewPassword'] != updated_info['ConfirmPassword']:
                QMessageBox.warning(self, 'Error', '新密码和确认密码不匹配！')
                return

            success = update_airline_info(updated_info)
            if success:
                QMessageBox.information(self, 'Success', '用户信息更新成功！')
                self.set_text_fields_editable(False)
            else:
                QMessageBox.warning(self, 'Error', '用户信息更新失败！')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'保存用户信息失败: {str(e)}')

    def cancel_editing(self):
        try:
            self.load_user_info(self.user_id)
            self.set_text_fields_editable(False)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'取消编辑失败: {str(e)}')


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
    airline_mainWindow = Airline_MainWindow(user_id = 'LFNL')
    sys.exit(app.exec_())
