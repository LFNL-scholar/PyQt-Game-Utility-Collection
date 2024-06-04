import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QDesktopWidget,
                             QMainWindow, QAction, qApp, QMenu, QTextEdit, QFileDialog, QFontDialog, QColorDialog, QInputDialog, QPlainTextEdit, QHBoxLayout)
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtCore import Qt


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(600, 400)  # 调整窗口大小
        self.center()

        self.setWindowTitle('LFNL TECH')
        self.setWindowIcon(QIcon('Icon.jpg'))

        self.textEdit = QTextEdit(self)  # 添加 QTextEdit 小部件
        self.setCentralWidget(self.textEdit)
        self.textEdit.setPlaceholderText("Welcome to LFNL")

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.lineNumberWidget = None  # 行号小部件
        self.currentFindText = ''  # 当前查找的文本

        self.show()

    def createActions(self):
        self.newAction = QAction(QIcon('new.png'), '新建', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('新建文件')
        self.newAction.triggered.connect(self.newFile)

        self.openAction = QAction(QIcon('open.png'), '打开', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('打开文件')
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QAction(QIcon('save.png'), '保存', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('保存文件')
        self.saveAction.triggered.connect(self.saveFile)

        self.printAction = QAction(QIcon('print.png'), '打印', self)
        self.printAction.setShortcut('Ctrl+P')
        self.printAction.setStatusTip('打印文件')
        self.printAction.triggered.connect(self.printFile)

        self.fontAction = QAction('字体', self)
        self.fontAction.setShortcut('Ctrl+T')
        self.fontAction.setStatusTip('选择字体')
        self.fontAction.triggered.connect(self.selectFont)

        self.bgColorAction = QAction('背景颜色', self)
        self.bgColorAction.setStatusTip('设置背景颜色')
        self.bgColorAction.triggered.connect(self.selectBgColor)

        self.undoAction = QAction('撤销', self)
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.setStatusTip('撤销最后一次操作')
        self.undoAction.triggered.connect(self.textEdit.undo)

        self.redoAction = QAction('重做', self)
        self.redoAction.setShortcut('Ctrl+Shift+Z')
        self.redoAction.setStatusTip('重做最后一次操作')
        self.redoAction.triggered.connect(self.textEdit.redo)

        self.copyAction = QAction('复制', self)
        self.copyAction.setShortcut('Ctrl+C')
        self.copyAction.setStatusTip('复制选中的文本')
        self.copyAction.triggered.connect(self.textEdit.copy)

        self.cutAction = QAction('剪切', self)
        self.cutAction.setShortcut('Ctrl+X')
        self.cutAction.setStatusTip('剪切选中的文本')
        self.cutAction.triggered.connect(self.textEdit.cut)

        self.pasteAction = QAction('粘贴', self)
        self.pasteAction.setShortcut('Ctrl+V')
        self.pasteAction.setStatusTip('粘贴剪贴板的内容')
        self.pasteAction.triggered.connect(self.textEdit.paste)

        self.findAction = QAction('查找', self)
        self.findAction.setShortcut('Ctrl+F')
        self.findAction.setStatusTip('查找文本')
        self.findAction.triggered.connect(self.findText)

        self.findNextAction = QAction('查找下一个', self)
        self.findNextAction.setShortcut('F3')
        self.findNextAction.setStatusTip('查找下一个匹配')
        self.findNextAction.triggered.connect(self.findNext)

        self.replaceAction = QAction('替换', self)
        self.replaceAction.setShortcut('Ctrl+H')
        self.replaceAction.setStatusTip('替换文本')
        self.replaceAction.triggered.connect(self.replaceText)

        self.wordCountAction = QAction('字数统计', self)
        self.wordCountAction.setStatusTip('统计字数和字符数')
        self.wordCountAction.triggered.connect(self.wordCount)

        self.lineNumbersAction = QAction('显示行号', self)
        self.lineNumbersAction.setStatusTip('显示行号')
        self.lineNumbersAction.triggered.connect(self.toggleLineNumbers)
        self.lineNumbersAction.setCheckable(True)

        self.wrapAction = QAction('自动换行', self)
        self.wrapAction.setStatusTip('自动换行')
        self.wrapAction.triggered.connect(self.toggleWrap)
        self.wrapAction.setCheckable(True)

        self.recentFilesMenu = QMenu('最近文件', self)
        self.recentFilesActions = []

    def createMenus(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.printAction)
        fileMenu.addMenu(self.recentFilesMenu)

        editMenu = menubar.addMenu('编辑')
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.findAction)
        editMenu.addAction(self.findNextAction)
        editMenu.addAction(self.replaceAction)
        editMenu.addAction(self.wordCountAction)

        formatMenu = menubar.addMenu('格式')
        formatMenu.addAction(self.fontAction)
        formatMenu.addAction(self.bgColorAction)
        formatMenu.addAction(self.lineNumbersAction)
        formatMenu.addAction(self.wrapAction)

    def createToolBars(self):
        self.toolbar = self.addToolBar('工具栏')
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.pasteAction)

    def createStatusBar(self):
        self.statusBar().showMessage('就绪')

    def newFile(self):
        self.textEdit.clear()

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "Text Files (*.txt);;All Files (*)",
                                                  options=options)
        if fileName:
            with open(fileName, 'r') as file:
                self.textEdit.setText(file.read())
            self.addRecentFile(fileName)

    def saveFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "Text Files (*.txt);;All Files (*)",
                                                  options=options)
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def printFile(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

    def selectFont(self):
        fontDialog = QFontDialog(self)
        fontDialog.setWindowIcon(QIcon('Icon.jpg'))  # 设置字体选择对话框的图标
        if fontDialog.exec_() == QFontDialog.Accepted:
            font = fontDialog.selectedFont()
            self.textEdit.setFont(font)

    def selectBgColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.textEdit.setStyleSheet(f"background-color: {color.name()};")

    def findText(self):
        text, ok = QInputDialog.getText(self, '查找', '输入要查找的文本:')
        if ok and text:
            self.currentFindText = text
            self.findNext()

    def findNext(self):
        text = self.currentFindText
        if text:
            cursor = self.textEdit.textCursor()
            document = self.textEdit.document()

            cursor = document.find(text, cursor)

            if cursor.isNull():
                QMessageBox.information(self, '未找到', f'未找到"{text}"')
                return

            cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)
            self.textEdit.setTextCursor(cursor)

    def replaceText(self):
        findText, ok = QInputDialog.getText(self, '查找', '输入要查找的文本:')
        if ok and findText:
            replaceText, ok = QInputDialog.getText(self, '替换', '输入替换后的文本:')
            if ok and replaceText:
                text = self.textEdit.toPlainText()
                self.textEdit.setText(text.replace(findText, replaceText))

    def wordCount(self):
        text = self.textEdit.toPlainText()
        wordCount = len(text.split())
        charCount = len(text)
        QMessageBox.information(self, '字数统计', f'单词数: {wordCount}\n字符数: {charCount}')

    def toggleLineNumbers(self):
        if self.lineNumbersAction.isChecked():
            self.addLineNumbers()
        else:
            self.removeLineNumbers()

    def addLineNumbers(self):
        if self.lineNumberWidget is None:
            self.lineNumberWidget = QPlainTextEdit(self)
            self.lineNumberWidget.setReadOnly(True)
            self.lineNumberWidget.setFixedWidth(50)
            self.lineNumberWidget.setLineWrapMode(QPlainTextEdit.NoWrap)
            self.lineNumberWidget.setStyleSheet("background-color: #f0f0f0;")
            self.lineNumberWidget.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")

        layout = QHBoxLayout()
        layout.addWidget(self.lineNumberWidget)
        layout.addWidget(self.textEdit)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.textEdit.blockCountChanged.connect(self.updateLineNumbers)
        self.textEdit.verticalScrollBar().valueChanged.connect(self.updateLineNumbers)

        self.updateLineNumbers()

    def removeLineNumbers(self):
        self.setCentralWidget(self.textEdit)
        if self.lineNumberWidget:
            self.lineNumberWidget.deleteLater()
            self.lineNumberWidget = None

    def updateLineNumbers(self):
        if self.lineNumberWidget:
            lineNumbers = "\n".join(str(i) for i in range(1, self.textEdit.blockCount() + 1))
            self.lineNumberWidget.setPlainText(lineNumbers)
            self.lineNumberWidget.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().value())

    def toggleWrap(self):
        if self.wrapAction.isChecked():
            self.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

    def addRecentFile(self, fileName):
        action = QAction(fileName, self)
        action.triggered.connect(lambda: self.openRecentFile(fileName))
        self.recentFilesActions.append(action)
        self.recentFilesMenu.addAction(action)

    def openRecentFile(self, fileName):
        with open(fileName, 'r') as file:
            self.textEdit.setText(file.read())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
