"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：购票用户主界面和功能的设计与实现
"""
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget, QPushButton, \
    QStackedWidget, QLineEdit, QComboBox, QDateEdit
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QCoreApplication

from SQLs import *
from Airline_Union_db import *
import Config as C

# 导入界面所需图片
from AAMS.UI import images_rc

# 全局变量


class User_MainWindow(QMainWindow):  # 步骤1: 登录成功后的窗口类
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id  # 记录当前用户的ID

        self.initUI()

    def initUI(self):

        uic.loadUi('UI/LogCataWin.ui', self)

        ## 获取侧边栏控件
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.flight_searchButton = self.findChild(QPushButton, 'Flight_SearchButton')
        self.homeButton = self.findChild(QPushButton, 'HomeButton')
        self.orders_Button = self.findChild(QPushButton, 'Orders_Button')
        self.travel_Service_Button = self.findChild(QPushButton, 'Travel_Service_Button')
        self.modify_Button = self.findChild(QPushButton, 'Modify_Button')
        self.about_us_Button = self.findChild(QPushButton, 'About_Us_Button')

        self.quit_Button = self.findChild(QPushButton, 'Quit_Button')

        # 设置初始页面为 Home
        self.stackedWidget.setCurrentIndex(0)

        # 连接按钮的点击事件到对应的方法
        self.flight_searchButton.clicked.connect(self.ToSearch)
        self.homeButton.clicked.connect(self.ToHome)
        self.orders_Button.clicked.connect(self.ToOrders)
        self.travel_Service_Button.clicked.connect(self.ToTravel)
        self.modify_Button.clicked.connect(self.ToModify)
        self.about_us_Button.clicked.connect(self.ToAboutUs)

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
        self.stackedWidget.setCurrentIndex(1)
        search_page = self.stackedWidget.currentWidget()

        self.departure_city_combobox = search_page.findChild(QComboBox, 'DepartureCityComboBox')
        self.arrival_city_combobox = search_page.findChild(QComboBox, 'ArrivalCityComboBox')
        self.populate_airports()

        search_button = search_page.findChild(QPushButton, 'SearchButton')
        search_button.clicked.connect(self.search_flights)

    def populate_airports(self):
        airports = get_airports_from_db()
        self.departure_city_combobox.clear()
        self.arrival_city_combobox.clear()

        for city, airport in airports:
            self.departure_city_combobox.addItem(f"{city} - {airport}")
            self.arrival_city_combobox.addItem(f"{city} - {airport}")

    def search_flights(self):
        departure_city_airport = self.departure_city_combobox.currentText().split(' - ')
        arrival_city_airport = self.arrival_city_combobox.currentText().split(' - ')
        departure_city = departure_city_airport[0]
        arrival_city = arrival_city_airport[0]
        departure_date = self.findChild(QDateEdit, 'DateEdit').date().toString(Qt.ISODate)
        # 添加搜索逻辑的代码


    # 我的订单界面
    def ToOrders(self):
        # 切换到我的订单页面
        self.stackedWidget.setCurrentIndex(2)

    # 出行服务界面
    def ToTravel(self):
        # 切换到出行服务页面
        self.stackedWidget.setCurrentIndex(3)

    # 修改资料界面
    def ToModify(self):
        # 切换到修改资料页面
        self.stackedWidget.setCurrentIndex(4)
        modify_page = self.stackedWidget.widget(4)

        self.cid_edit = modify_page.findChild(QLineEdit, 'cidEdit')
        self.cname_edit = modify_page.findChild(QLineEdit, 'cnameEdit')
        self.realname_edit = modify_page.findChild(QLineEdit, 'realnameEdit')
        self.telephonenum_edit = modify_page.findChild(QLineEdit, 'telephonenumEdit')
        self.csid_edit = modify_page.findChild(QLineEdit, 'csidEdit')
        self.csex_edit = modify_page.findChild(QLineEdit, 'csexEdit')

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

    def set_text_fields_editable(self, editable):
        self.cid_edit.setReadOnly(not editable)
        self.cname_edit.setReadOnly(not editable)
        self.realname_edit.setReadOnly(not editable)
        self.telephonenum_edit.setReadOnly(not editable)
        self.csid_edit.setReadOnly(not editable)
        self.csex_edit.setReadOnly(not editable)
        self.new_password_edit.setReadOnly(not editable)
        self.confirm_password_edit.setReadOnly(not editable)

    def enable_editing(self):
        self.set_text_fields_editable(True)

    def load_user_info(self, cid):
        user_info = get_user_info(cid)

        self.cid_edit.setText(user_info[0])
        self.cname_edit.setText(user_info[1])
        self.realname_edit.setText(user_info[2])
        self.telephonenum_edit.setText(user_info[3])
        self.csid_edit.setText(user_info[4])
        self.csex_edit.setText(user_info[5])

    def save_user_info(self):
        updated_info = {
            'CID': self.cid_edit.text(),
            'Cname': self.cname_edit.text(),
            'Realname': self.realname_edit.text(),
            'TelephoneNum': self.telephonenum_edit.text(),
            'Csid': self.csid_edit.text(),
            'Csex': self.csex_edit.text(),
            'NewPassword': self.new_password_edit.text(),  # 新密码
            'ConfirmPassword': self.confirm_password_edit.text()  # 确认密码
        }

        if updated_info['NewPassword'] != updated_info['ConfirmPassword']:
            QMessageBox.warning(self, 'Error', '新密码和确认密码不匹配！')
            return

        success = update_user_info(updated_info)
        if success:
            QMessageBox.information(self, 'Success', '用户信息更新成功！')
            self.set_text_fields_editable(False)
        else:
            QMessageBox.warning(self, 'Error', '用户信息更新失败！')

    def cancel_editing(self):
        self.load_user_info(self.user_id)
        self.set_text_fields_editable(False)

    # 关于我们界面
    def ToAboutUs(self):
        # 切换到关于我们页面
        self.stackedWidget.setCurrentIndex(5)


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
    user_mainWindow = User_MainWindow(user_id = 'LFNL')
    sys.exit(app.exec_())
