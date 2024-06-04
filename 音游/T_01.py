import sys
import random
import time
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDesktopWidget, QVBoxLayout, QLabel
import pygame


class RhythmGame(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('音游')
        self.setGeometry(300, 300, 800, 600)
        self.center()

        self.gameBoard = GameBoard(self)
        self.setCentralWidget(self.gameBoard)

        self.statusbar = self.statusBar()
        self.gameBoard.scoreSignal[str].connect(self.updateStatusBar)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updateStatusBar(self, score):
        self.statusbar.showMessage(score)


class GameBoard(QFrame):
    scoreSignal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.setFocusPolicy(Qt.StrongFocus)
        self.score = 0
        self.notes = []
        self.note_speed = 5
        self.spawn_note()
        self.timer.start(30)
        self.start_time = time.time()
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("WYY.mp3")
        pygame.mixer.music.play()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the hit area
        self.drawHitArea(painter)

        for note in self.notes:
            self.drawSquare(painter, note[0], note[1])

    def drawSquare(self, painter, x, y):
        color = QColor(255, 0, 0)
        painter.fillRect(x, y, 20, 20, color)

    def drawHitArea(self, painter):
        color = QColor(200, 200, 200)
        painter.fillRect(0, 550, self.width(), 50, color)

    def spawn_note(self):
        self.notes.append([random.randint(50, 750), 0])

    def updateGame(self):
        self.updateNotes()
        self.update()
        self.check_collision()

    def updateNotes(self):
        for note in self.notes:
            note[1] += self.note_speed
        if time.time() - self.start_time > 1:
            self.spawn_note()
            self.start_time = time.time()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Space:
            self.check_hit()

    def check_hit(self):
        for note in self.notes:
            if 550 < note[1] < 600:
                self.notes.remove(note)
                self.score += 10
                self.scoreSignal.emit('Score: ' + str(self.score))
                break

    def check_collision(self):
        for note in self.notes:
            if note[1] > 600:
                self.notes.remove(note)
                self.score -= 10
                self.scoreSignal.emit('Score: ' + str(self.score))
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RhythmGame()
    sys.exit(app.exec_())
