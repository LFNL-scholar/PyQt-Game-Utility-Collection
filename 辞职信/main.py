import os
import random
 
import pyautogui as pag
 
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QWidget
import threading
class Stats(QWidget):
    btn_signal = pyqtSignal() # 定义时钟的信号
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("my.ui")
        self.resize(960, 700) # 设置屏幕宽高
        self.x_big = 600 # 设置控件在屏幕的位置
        self.y_big = 200
        self.ui.move(self.x_big, self.y_big) # 移动到指定位置
        self.btn_signal.connect(self.move)
        self.x = 380 # 确定按钮初始位置
        self.y = 300
        self.xl = 93 # 确定按钮的宽高
        self.yl = 28
 
        # 2784  59
        print(self.ui.geometry().width())
        t = threading.Thread(target=self.get_move_thread)
        t.start()
 
    def get_move_thread(self):
        try:
            while True:
                    x,y = pag.position() #返回鼠标的坐标
                    posStr="Position:"+str(x).rjust(4)+','+str(y).rjust(4)
                    btn_x = self.x+self.x_big+3 # 由于边框有尺寸，需要单独加入
                    btn_y = self.y+self.y_big+40
                    # print('====================')
                    # print('x:{}'.format(x))
                    # print('btn_x:{}'.format(btn_x))
                    # print('btn_x+xl:{}'.format(btn_x + self.xl))
                    # print('y:{}'.format(y))
                    # print('btn_y:{}'.format(btn_y))
                    # print('btn_y+yl:{}'.format(btn_y + self.yl))
                    # print('====================')
                    # if x >=btn_x & x <=(btn_x+self.xl) & y>=btn_y &y<=(btn_y+self.yl):
                    if x >=btn_x :
                        if x <=(btn_x+self.xl):
                            if y>=btn_y:
                                if y<=(btn_y+self.yl):
                                    # print('======enter')
                                    self.btn_signal.emit()
                    # print (posStr)#打印坐标
                    # time.sleep(2)
                    # os.system('cls')#清空屏幕
        except  KeyboardInterrupt:
            print ('end....')
 
    def move(self):
        self.x = random.randint(30, 500)
        self.y = random.randint(30, 450)
        # print(self.x)
        # print(self.y)
        self.ui.move_btn.move(self.x, self.y)
if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()