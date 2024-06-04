import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QDesktopWidget, QMessageBox

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 400)
        self.center()

        self.setWindowTitle('薪资统计')
        self.setWindowIcon(QIcon('Icon.jpg'))

        self.textEdit = QPlainTextEdit(self)
        self.textEdit.setPlaceholderText("请输入新资表")
        self.textEdit.setGeometry(10, 25, 300, 350)

        self.button = QPushButton('统计', self)
        self.button.setGeometry(350, 80, 100, 40)
        self.button.clicked.connect(self.onButtonClicked)

        self.show()

    def onButtonClicked(self):

        info = self.textEdit.toPlainText()
        # 薪资20000以上和以下的人员名单
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')
            parts = [p for p in parts if p]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self, '统计结果',
                          f'''薪资20000以上的有：\n {salary_above_20k}
                          \n 薪资20000以下的有： \n {salary_below_20k}''')


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# 测试数据
'''
薛蟠     4560 25
薛蝌     4460 25
薛宝钗   35776 23
薛宝琴   14346 18
王夫人   43360 45
王熙凤   24460 25
王子腾   55660 45
王仁     15034 65
尤二姐   5324 24
贾芹     5663 25
贾兰     13443 35
贾芸     4522 25
尤三姐   5905 22
贾珍     54603 35
'''