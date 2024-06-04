import sys
import random
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDesktopWidget, QHBoxLayout, QLabel

class SnakeGame(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('贪吃蛇')
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.center()

        self.snakeboard = SnakeBoard(self)
        self.setCentralWidget(self.snakeboard)

        self.statusbar = self.statusBar()
        self.snakeboard.scoreSignal[str].connect(self.updateStatusBar)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updateStatusBar(self, score):
        self.statusbar.showMessage(score)

class SnakeBoard(QFrame):

    boardWidth = 30
    boardHeight = 20
    speed = 150

    scoreSignal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)
        self.snake = [[5, 10], [4, 10], [3, 10]]
        self.food = [10, 10]
        self.direction = Qt.Key_Right
        self.score = 0
        self.gameOver = False
        self.placeFood()
        self.startGame()

    def startGame(self):
        self.score = 0
        self.snake = [[5, 10], [4, 10], [3, 10]]
        self.direction = Qt.Key_Right
        self.placeFood()
        self.timer.start(self.speed, self)

    def placeFood(self):
        while True:
            x = random.randint(0, self.boardWidth - 1)
            y = random.randint(0, self.boardHeight - 1)
            if [x, y] not in self.snake:
                self.food = [x, y]
                break

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardTop = rect.bottom() - self.boardHeight * self.squareHeight()

        for pos in self.snake:
            self.drawSquare(painter, rect.left() + pos[0] * self.squareWidth(),
                            boardTop + pos[1] * self.squareHeight(), QColor(0, 255, 0))

        self.drawSquare(painter, rect.left() + self.food[0] * self.squareWidth(),
                        boardTop + self.food[1] * self.squareHeight(), QColor(255, 0, 0))

    def drawSquare(self, painter, x, y, color):
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, self.squareHeight() - 2, color)

    def squareWidth(self):
        return self.contentsRect().width() // self.boardWidth

    def squareHeight(self):
        return self.contentsRect().height() // self.boardHeight

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_P:
            self.pauseGame()
        elif key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            self.changeDirection(key)
        elif key == Qt.Key_Space:
            self.startGame()

    def changeDirection(self, key):
        if (key == Qt.Key_Left and self.direction != Qt.Key_Right) or \
           (key == Qt.Key_Right and self.direction != Qt.Key_Left) or \
           (key == Qt.Key_Up and self.direction != Qt.Key_Down) or \
           (key == Qt.Key_Down and self.direction != Qt.Key_Up):
            self.direction = key

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if not self.gameOver:
                self.move()
            self.update()
        else:
            super(SnakeBoard, self).timerEvent(event)

    def move(self):
        head = self.snake[0][:]
        if self.direction == Qt.Key_Left:
            head[0] -= 1
        elif self.direction == Qt.Key_Right:
            head[0] += 1
        elif self.direction == Qt.Key_Up:
            head[1] -= 1
        elif self.direction == Qt.Key_Down:
            head[1] += 1

        if head in self.snake or head[0] < 0 or head[0] >= self.boardWidth or head[1] < 0 or head[1] >= self.boardHeight:
            self.timer.stop()
            self.gameOver = True
            self.scoreSignal.emit('Game Over! Your score: ' + str(self.score))
            return

        self.snake.insert(0, head)
        if head == self.food:
            self.score += 1
            self.scoreSignal.emit('Score: ' + str(self.score))
            self.placeFood()
        else:
            self.snake.pop()

    def pauseGame(self):
        if self.timer.isActive():
            self.timer.stop()
            self.scoreSignal.emit('Paused')
        else:
            self.timer.start(self.speed, self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SnakeGame()
    sys.exit(app.exec_())
