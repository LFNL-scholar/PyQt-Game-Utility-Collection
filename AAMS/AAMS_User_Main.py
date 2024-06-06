"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：购票用户主界面和功能的设计与实现
"""
import os
import sys

import datetime

from datetime import datetime, timedelta

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


class User_MainWindow(QMainWindow):
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
        self.date_edit = search_page.findChild(QDateEdit, 'DateEdit')
        self.populate_airports()

        search_button = search_page.findChild(QPushButton, 'SearchButton')
        search_button.clicked.connect(self.match_flights)

    # 从数据库中获取机场数据
    def populate_airports(self):
        airports = get_airports_from_db()
        if airports:
            self.departure_city_combobox.clear()
            self.arrival_city_combobox.clear()

            for city, airport in airports:
                self.departure_city_combobox.addItem(f"{city} - {airport}")
                self.arrival_city_combobox.addItem(f"{city} - {airport}")
        else:
            QMessageBox.warning(self, 'Error', '无法从数据库获取机场信息。')

    # 匹配符合条件的航班数据
    def match_flights(self):
        departure_city_airport = self.departure_city_combobox.currentText().split(' - ')
        arrival_city_airport = self.arrival_city_combobox.currentText().split(' - ')
        departure_airport = departure_city_airport[1]
        arrival_airport = arrival_city_airport[1]
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")

        try:
            flights_data = search_flights(departure_airport, arrival_airport, selected_date)
        except Exception as e:
            QMessageBox.information(self, 'NO', '匹配错误')

        if flights_data:
            self.show_flights_result(flights_data)
        else:
            QMessageBox.information(self, 'No Flights', '未找到符合条件的航班。')

    # 跳转到航班搜索结果界面
    def show_flights_result(self, flights_data):
        # 获取结果页部件
        self.stackedWidget.setCurrentIndex(6)
        result_page = self.stackedWidget.currentWidget()

        # 获取表格控件
        table = result_page.findChild(QTableWidget, 'ResultTableWidget')
        if not table:
            QMessageBox.warning(self, 'Error', '未找到结果表格。')
            return

        table.setRowCount(len(flights_data))
        table.setColumnCount(11)

        # 填充表格数据
        for row_num, flight in enumerate(flights_data):

            # 填充航班数据
            for col_num, data in enumerate(flight):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_num, col_num, item)

            # 添加选择控件
            select_checkbox = QCheckBox()
            select_checkbox.stateChanged.connect(
                lambda state, f = flight: self.handle_checkbox_state_change(state, f))
            select_checkbox_widget = QWidget()
            layout = QHBoxLayout(select_checkbox_widget)
            layout.addWidget(select_checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            select_checkbox_widget.setLayout(layout)
            table.setCellWidget(row_num, 10, select_checkbox_widget)  # 选择控件放在最后一列

        # 设置特定列的宽度
        table.setColumnWidth(0, 70)  # 航班编号
        table.setColumnWidth(1, 70)  # 出发地点
        table.setColumnWidth(2, 70)  # 到达地点
        table.setColumnWidth(3, 100)  # 出发机场
        table.setColumnWidth(4, 100)  # 到达机场
        table.setColumnWidth(5, 80)  # 起飞日期
        table.setColumnWidth(6, 80)  # 起飞时间
        table.setColumnWidth(7, 80)  # 飞行时间
        table.setColumnWidth(8, 80)  # 机型
        table.setColumnWidth(9, 80)  # 票价
        table.setColumnWidth(10, 80)  # 选择


        # 更新表格数据后，确保页面显示正确
        self.stackedWidget.setCurrentIndex(6)

        # 获取确认按钮并连接其点击事件
        confirm_button = result_page.findChild(QPushButton, 'ConfirmButton')
        confirm_button.clicked.connect(self.confirm_selection)

    # 处理复选框的状态变化
    def handle_checkbox_state_change(self, state, flight):
        if state == Qt.Checked:
            self.selected_flight = flight
        else:
            self.selected_flight = None

    # 确认按钮的点击事件处理
    def confirm_selection(self):
        if not self.selected_flight:
            QMessageBox.warning(self, 'Error', '请选择一个航班。')
            return

        self.ToPurchase()

    # 跳转到购买页面
    def ToPurchase(self):
        self.stackedWidget.setCurrentIndex(7)
        purchase_page = self.stackedWidget.currentWidget()

        # 获取各个 QLabel 对象
        flight_number_label = purchase_page.findChild(QLabel, 'FlightNumberLabel')
        plane_type_label = purchase_page.findChild(QLabel, 'PlaneTypeLabel')
        departure_date_label = purchase_page.findChild(QLabel, 'DepartureDateLabel')
        departure_time_label = purchase_page.findChild(QLabel, 'DepartureTimeLabel')
        arrival_time_label = purchase_page.findChild(QLabel, 'ArrivalTimeLabel')
        departure_airport_label = purchase_page.findChild(QLabel, 'DepartureAirportLabel')
        arrival_airport_label = purchase_page.findChild(QLabel, 'ArrivalAirportLabel')
        price_label = purchase_page.findChild(QLabel, 'PriceLabel')

        purchase_button = purchase_page.findChild(QPushButton, 'PurchaseButton')
        purchase_button.clicked.connect(self.purchase_ticket)

        # 假设 self.selected_flight 包含一个元组，依次包含航班编号、出发地点、到达地点、出发机场、到达机场、
        # 出发日期、起飞时间、飞行时间、飞机类型和价格
        (flight_id, departure_place, arrival_place, departure_airport, arrival_airport, departure_date,
         takeoff_time, total_time, plane_type, price) = self.selected_flight

        # 设置各个 QLabel 的文本
        flight_number_label.setText(f"{flight_id}")
        plane_type_label.setText(f"{plane_type}")
        departure_date_label.setText(f"{departure_date}")
        departure_time_label.setText(f"{takeoff_time}")
        arrival_time_label.setText(f"{takeoff_time + total_time}")
        departure_airport_label.setText(f"{departure_airport}")
        arrival_airport_label.setText(f"{arrival_airport}")
        price_label.setText(f"￥ {price}")


        self.WritePassengers()

    def WritePassengers(self):

        purchase_page = self.stackedWidget.currentWidget()

        self.selectcomboBox = purchase_page.findChild(QComboBox, 'SelectcomboBox')

        items = ["1人", "2人", "3人"]

        # 检查是否已经有项目添加，如果没有项目才添加
        if self.selectcomboBox.count() == 0:
            self.selectcomboBox.addItems(items)

        # 连接信号槽，当选择人数时触发相应的页面切换
        self.selectcomboBox.currentIndexChanged.connect(self.on_combobox_changed)

    # 槽函数
    def on_combobox_changed(self):
        purchase_page = self.stackedWidget.currentWidget()

        # 获取内嵌的 QStackedWidget
        inner_stacked_widget = purchase_page.findChild(QStackedWidget, 'InnerStackedWidget')
        if inner_stacked_widget:
            selected_index = self.selectcomboBox.currentIndex()
            inner_stacked_widget.setCurrentIndex(selected_index)

    def purchase_ticket(self):
        purchase_page = self.stackedWidget.currentWidget()

        # 获取内嵌的 QStackedWidget
        inner_stacked_widget = purchase_page.findChild(QStackedWidget, 'InnerStackedWidget')
        if not inner_stacked_widget:
            QMessageBox.warning(self, 'Error', '找不到内嵌的 QStackedWidget')
            return

        # 获取第一个页面
        first_page = inner_stacked_widget.widget(0)

        # 获取第一个页面的 QLineEdit 对象
        name_edit = first_page.findChild(QLineEdit, 'NameLineEdit')
        sex_edit = first_page.findChild(QLineEdit, 'SexLineEdit')
        id_edit = first_page.findChild(QLineEdit, 'IDLineEdit')
        seat_num_edit = first_page.findChild(QLineEdit, 'SeatNumLineEdit')

        # 获取用户输入的数据
        name = name_edit.text()
        sex = sex_edit.text()
        psid = id_edit.text()
        seat_num = seat_num_edit.text()

        # 检查输入是否为空
        if not name or not sex or not psid or not seat_num:
            QMessageBox.warning(self, 'Error', '所有内容都是必填项，请填写完整信息。')
            return

        # 检查身份证号是否为18位字符串
        if len(psid) != 18:
            QMessageBox.warning(self, 'Error', '身份证号必须是18位。')
            return

        cid = self.user_id  # 假设当前用户ID存储在self.current_user_id
        flight_id = self.selected_flight[0]  # 假设航班编号是 self.selected_flight 的第一个元素
        price = self.selected_flight[-1]  # 假设价格是 self.selected_flight 的最后一个元素

        # 生成订单编号
        order_id = generate_order_id()
        payment_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:

            # 插入订单信息
            if not insert_order(order_id, price, 'Y', payment_time, cid):  # 'Y'表示已支付状态
                raise Exception('插入订单信息失败，请重试。')

            # 插入乘客信息
            insert_passenger(order_id, psid, name, sex)

            # 插入机票信息
            if not insert_ticket(flight_id, seat_num, order_id, psid, price):
                raise Exception('插入机票信息失败，请重试。')

            QMessageBox.information(self, 'Success', '购买成功！')

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


        print(name, sex, psid, seat_num)



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
