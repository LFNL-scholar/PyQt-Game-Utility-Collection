import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QSlider, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
import pygame


class MusicPlayer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Music Player')
        self.setGeometry(300, 300, 600, 400)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        # Album Art
        self.albumArt = QLabel(self)
        self.albumArt.setPixmap(QPixmap('default_album_art.png').scaled(200, 200, Qt.KeepAspectRatio))
        self.albumArt.setAlignment(Qt.AlignCenter)

        # Title
        self.title = QLabel('No song playing', self)
        self.title.setAlignment(Qt.AlignCenter)

        # Slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setValue(0)
        self.slider.sliderMoved.connect(self.setPosition)

        # Buttons
        self.playButton = QPushButton('Play', self)
        self.playButton.clicked.connect(self.playMusic)

        self.pauseButton = QPushButton('Pause', self)
        self.pauseButton.clicked.connect(self.pauseMusic)

        self.stopButton = QPushButton('Stop', self)
        self.stopButton.clicked.connect(self.stopMusic)

        self.openButton = QPushButton('Open', self)
        self.openButton.clicked.connect(self.openFile)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.openButton)

        # Timer
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateSlider)

        # Layout
        self.layout.addWidget(self.albumArt)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.slider)
        self.layout.addLayout(buttonLayout)

        # Pygame mixer
        pygame.init()
        pygame.mixer.init()

        self.show()

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open MP3 File", "", "MP3 Files (*.mp3);;All Files (*)", options=options)
        if fileName:
            self.musicFile = fileName
            self.title.setText(os.path.basename(fileName))
            self.playMusic()

    def playMusic(self):
        try:
            if hasattr(self, 'musicFile'):
                pygame.mixer.music.load(self.musicFile)
                pygame.mixer.music.play()
                self.timer.start()
                self.slider.setMaximum(int(pygame.mixer.Sound(self.musicFile).get_length()))
        except pygame.error as e:
            self.title.setText(f"Error: {e}")

    def pauseMusic(self):
        try:
            pygame.mixer.music.pause()
        except pygame.error as e:
            self.title.setText(f"Error: {e}")

    def stopMusic(self):
        try:
            pygame.mixer.music.stop()
            self.timer.stop()
            self.slider.setValue(0)
        except pygame.error as e:
            self.title.setText(f"Error: {e}")

    def setPosition(self, position):
        try:
            pygame.mixer.music.set_pos(position)
        except pygame.error as e:
            self.title.setText(f"Error: {e}")

    def updateSlider(self):
        try:
            self.slider.setValue(int(pygame.mixer.music.get_pos() / 1000))
        except pygame.error as e:
            self.title.setText(f"Error: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    sys.exit(app.exec_())
