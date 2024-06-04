import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDesktopWidget
from PyQt5 import uic

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        uic.loadUi('UI/Salary.ui', self)
        self.button.clicked.connect(self.onButtonClicked)
        self.check.clicked.connect(self.onCheckClicked)

        self.setWindowIcon(QIcon('Icon.jpg'))
        self.show()

    def onCheckClicked(self):
        print('你好~')

    def onButtonClicked(self):
        info = self.textEdit.toPlainText()

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

    # 关闭窗口提示
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "亲亲，您真的要离开我嘛~ 呜呜",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
