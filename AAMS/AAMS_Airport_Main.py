"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：机场管理员主界面和功能的设计与实现
"""
import os
import sys

import datetime

from datetime import datetime, timedelta
from wsgiref import headers

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget, QPushButton, \
    QStackedWidget, QLineEdit, QComboBox, QDateEdit, QVBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox, \
    QHBoxLayout, QLabel, QTimeEdit
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QCoreApplication

from SQLs import *
from Airline_Union_db import *

import Config as C

# 导入界面所需图片
from AAMS.UI import images_rc

# 全局变量

class Airport_MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id  # 记录当前用户的ID

        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Airport_User.ui', self)

        ## 获取控件
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.homeButton = self.findChild(QPushButton, 'HomeButton')
        self.flight_schedulerButton = self.findChild(QPushButton, 'Flight_schedulerButton')
        self.modify_Button = self.findChild(QPushButton, 'modifyButton')
        self.quit_Button = self.findChild(QPushButton, 'Quit_Button')

        # 设置初始页面为 Home
        self.stackedWidget.setCurrentIndex(0)

        # 连接按钮的点击事件到对应的方法
        self.homeButton.clicked.connect(self.ToHome)
        self.flight_schedulerButton.clicked.connect(self.ToSearch)
        self.modify_Button.clicked.connect(self.ToModify)

        # 退出登录
        self.quit_Button.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        self.show()

    # 主页面
    def ToHome(self):
        # 切换到主页面
        self.stackedWidget.setCurrentIndex(0)

    def ToSearch(self):
        amid = self.user_id
        # print(search_aname_by_amid(amid))
        try:
            aname = search_aname_by_amid(amid)
            if not aname:
                raise ValueError("未找到对应的机场名")
        except Exception as e:
            QMessageBox.information(self, 'Error', f'查询机场名时出错: {e}')
            return

        try:
            flights_data = search_Airport_flights(aname)
            print(flights_data)  # Debugging line
        except Exception as e:
            QMessageBox.information(self, 'NO', '匹配错误')

        if flights_data:
            self.ToScheduler(flights_data)
        else:
            QMessageBox.information(self, 'No Flights', '未找到符合条件的航班_2')


    # 搜索调度界面
    def ToScheduler(self, flights_data):
        try:
            # 切换到调度页面
            self.stackedWidget.setCurrentIndex(1)
            result_page = self.stackedWidget.currentWidget()

            # 获取表格控件
            table = result_page.findChild(QTableWidget, 'ResultTableWidget')
            if not table:
                QMessageBox.warning(self, 'Error', '未找到结果表格。')
                return

            table.setRowCount(len(flights_data))
            table.setColumnCount(10)

            self.selected_flight = None  # 初始化selected_flight为None

            # 填充表格数据
            for row_num, flight in enumerate(flights_data):
                for col_num, data in enumerate(flight):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(row_num, col_num, item)

                # 添加选择控件
                select_checkbox = QCheckBox()
                select_checkbox.stateChanged.connect(
                    lambda state, row = row_num, f = flight: self.handle_checkbox_state_change(state, row, f))
                select_checkbox_widget = QWidget()
                layout = QHBoxLayout(select_checkbox_widget)
                layout.addWidget(select_checkbox)
                layout.setAlignment(Qt.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                select_checkbox_widget.setLayout(layout)
                table.setCellWidget(row_num, 9, select_checkbox_widget)  # 选择控件放在最后一列

            # 设置特定列的宽度
            table.setColumnWidth(0, 70)  # 航班编号
            table.setColumnWidth(1, 70)  # 出发地点
            table.setColumnWidth(2, 70)  # 到达地点
            table.setColumnWidth(3, 110)  # 出发机场
            table.setColumnWidth(4, 110)  # 到达机场
            table.setColumnWidth(5, 80)  # 起飞日期
            table.setColumnWidth(6, 80)  # 起飞时间
            table.setColumnWidth(7, 80)  # 飞行时间
            table.setColumnWidth(8, 80)  # 机型
            table.setColumnWidth(9, 80)  # 选择

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'调度界面加载时出错: {e}')

        # 获取确认按钮并连接其点击事件
        schedulerButton = result_page.findChild(QPushButton, 'SchedulerButton')
        schedulerButton.clicked.connect(self.confirm_selection)

    # 处理复选框的状态变化
    def handle_checkbox_state_change(self, state, row, flight):
        try:
            table = self.stackedWidget.currentWidget().findChild(QTableWidget, 'ResultTableWidget')
            if state == Qt.Checked:
                for i in range(table.rowCount()):
                    if i != row:
                        checkbox_widget = table.cellWidget(i, 9)
                        if checkbox_widget:  # 确保找到的控件存在
                            checkbox = checkbox_widget.findChild(QCheckBox)
                            checkbox.setChecked(False)
                self.selected_flight = flight
            elif state == Qt.Unchecked and self.selected_flight == flight:
                self.selected_flight = None
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'复选框状态变化处理时出错: {e}')

    # 确认按钮的点击事件处理
    def confirm_selection(self):
        try:
            if self.selected_flight is None:
                QMessageBox.warning(self, 'Error', '请选择一个航班。')
                return
            self.modify_selection()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'确认选择时出错: {e}')


    def modify_selection(self):
        # 切换到调度页面
        self.stackedWidget.setCurrentIndex(1)
        result_page = self.stackedWidget.currentWidget()

        # 获取QDateEdit和QTimeEdit控件
        date_edit = result_page.findChild(QDateEdit, 'dateEdit')
        departure_time_edit = result_page.findChild(QTimeEdit, 'departureTimeEdit')
        flight_time_edit = result_page.findChild(QTimeEdit, 'flightTimeEdit')

        # 获取确认按钮并连接其点击事件
        schedulerButton = result_page.findChild(QPushButton, 'SchedulerButton')
        schedulerButton.clicked.connect(lambda: self.on_confirm(date_edit, departure_time_edit, flight_time_edit))

    def on_confirm(self, date_edit, departure_time_edit, flight_time_edit):
        # 检查QDateEdit和QTimeEdit是否全部填写
        if not date_edit.date().isValid() or not departure_time_edit.time().isValid() or not flight_time_edit.time().isValid():
            QMessageBox.warning(self, 'Incomplete Information', '请填写完整的起飞日期和时间以及飞行时间。')
            return

        # 获取填写的值
        flight_date = date_edit.date().toString('yyyy-MM-dd')
        departure_time = departure_time_edit.time().toString('HH:mm:ss')
        flight_time = flight_time_edit.time().toString('HH:mm:ss')

        flight_id = self.get_selected_flight_id()
        print(flight_id)


        # 更新数据库
        try:
            update_flight_details(flight_id, flight_date, departure_time, flight_time)
            QMessageBox.information(self, 'Success', '航班信息已成功更新。')
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'更新数据库时发生错误: {e}')

    # 示例函数，假设航班信息在一个 QTableWidget 中
    def get_selected_flight_id(self):
        self.stackedWidget.setCurrentIndex(1)
        result_page = self.stackedWidget.currentWidget()
        table = result_page.findChild(QTableWidget, 'ResultTableWidget')

        if not table:
            return None

        for row in range(table.rowCount()):
            item = table.cellWidget(row, 9)  # 复选框在第9列
            if item:
                checkbox = item.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    flight_id_item = table.item(row, 0)  # 航班编号在第0列
                    if flight_id_item:
                        return flight_id_item.text()
        return None



    # 修改资料界面
    def ToModify(self):
        try:
            # 切换到修改资料页面
            self.stackedWidget.setCurrentIndex(2)
            modify_page = self.stackedWidget.widget(2)

            self.realname_edit = modify_page.findChild(QLineEdit, 'realnameEdit')
            self.amsex_edit = modify_page.findChild(QLineEdit, 'amsexEdit')
            self.amid_edit = modify_page.findChild(QLineEdit, 'amidEdit')
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
            self.amid_edit.setReadOnly(not editable)
            self.realname_edit.setReadOnly(not editable)
            self.amsex_edit.setReadOnly(not editable)
            self.new_password_edit.setReadOnly(not editable)
            self.confirm_password_edit.setReadOnly(not editable)
        except AttributeError as e:
            QMessageBox.warning(self, 'Error', f'设置文本框状态失败: {str(e)}')

    def enable_editing(self):
        try:
            self.set_text_fields_editable(True)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'启用编辑模式失败: {str(e)}')

    def load_user_info(self, amid):
        try:
            user_info = get_airport_manager_info(amid)
            if not user_info:
                raise ValueError("未找到用户信息")

            self.realname_edit.setText(user_info[0])
            self.amsex_edit.setText(user_info[1])
            self.amid_edit.setText(user_info[2])
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'加载用户信息失败: {str(e)}')

    def save_user_info(self):
        try:
            updated_info = {
                'AMID': self.amid_edit.text(),
                'AMname': self.realname_edit.text(),
                'AMsex': self.amsex_edit.text(),
                'NewPassword': self.new_password_edit.text(),  # 新密码
                'ConfirmPassword': self.confirm_password_edit.text()  # 确认密码
            }

            if updated_info['NewPassword'] != updated_info['ConfirmPassword']:
                QMessageBox.warning(self, 'Error', '新密码和确认密码不匹配！')
                return

            success = update_airport_manager_info(updated_info)
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
    airport_mainWindow = Airport_MainWindow(user_id = 'LFNL')
    sys.exit(app.exec_())
