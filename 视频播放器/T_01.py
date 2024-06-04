import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Player')
        self.setGeometry(300, 300, 800, 600)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        # Video display label
        self.videoLabel = QLabel(self)
        self.layout.addWidget(self.videoLabel)

        # Control buttons
        self.openButton = QPushButton('Open', self)
        self.openButton.clicked.connect(self.openFile)
        self.layout.addWidget(self.openButton)

        self.playButton = QPushButton('Play', self)
        self.playButton.clicked.connect(self.playVideo)
        self.layout.addWidget(self.playButton)

        self.pauseButton = QPushButton('Pause', self)
        self.pauseButton.clicked.connect(self.pauseVideo)
        self.layout.addWidget(self.pauseButton)

        self.stopButton = QPushButton('Stop', self)
        self.stopButton.clicked.connect(self.stopVideo)
        self.layout.addWidget(self.stopButton)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)

        self.cap = None
        self.isPlaying = False

        self.show()

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.avi *.mp4 *.mov);;All Files (*)", options=options)
        if fileName:
            self.videoFile = fileName
            self.cap = cv2.VideoCapture(self.videoFile)
            self.isPlaying = False

    def playVideo(self):
        if self.cap:
            self.isPlaying = True
            self.timer.start(30)

    def pauseVideo(self):
        self.isPlaying = False
        self.timer.stop()

    def stopVideo(self):
        self.isPlaying = False
        self.timer.stop()
        self.cap.release()
        self.videoLabel.clear()

    def updateFrame(self):
        if self.cap and self.isPlaying:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.videoLabel.setPixmap(pixmap)
            else:
                self.stopVideo()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec_())
