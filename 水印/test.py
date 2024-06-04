import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageDraw, ImageFont

class WatermarkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('Watermark Adder')

        # 创建用于显示图像的标签
        self.label = QLabel(self)
        self.label.setFixedSize(800, 600)

        # 创建上传图像的按钮
        self.btnUpload = QPushButton('Upload Image', self)
        self.btnUpload.clicked.connect(self.uploadImage)

        # 创建预览水印的按钮
        self.btnPreviewWatermark = QPushButton('Preview Watermark', self)
        self.btnPreviewWatermark.clicked.connect(self.previewWatermark)

        # 创建确认保存的按钮
        self.btnSaveWatermark = QPushButton('Save Watermark', self)
        self.btnSaveWatermark.clicked.connect(self.saveWatermark)

        # 创建水印颜色选择按钮
        self.blackRadio = QRadioButton('Transparent Black', self)
        self.whiteRadio = QRadioButton('Transparent White', self)
        self.blackRadio.setChecked(True)  # 默认选择黑色

        # 创建按钮组
        self.colorGroup = QButtonGroup(self)
        self.colorGroup.addButton(self.blackRadio)
        self.colorGroup.addButton(self.whiteRadio)

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.btnUpload)
        buttonLayout.addWidget(self.btnPreviewWatermark)
        buttonLayout.addWidget(self.btnSaveWatermark)
        layout.addLayout(buttonLayout)

        layout.addWidget(self.blackRadio)
        layout.addWidget(self.whiteRadio)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.imagePath = None  # 初始化图像路径为空
        self.previewImage = None  # 初始化预览图像为空

    def uploadImage(self):
        # 打开文件对话框，选择图像文件
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                  "Images (*.png *.xpm *.jpg *.jpeg);;All Files (*)", options=options)
        if fileName:
            # 设置选中的图像路径
            self.imagePath = fileName
            # 显示上传的图像
            pixmap = QPixmap(fileName)
            self.label.setPixmap(pixmap.scaled(self.label.size(), aspectRatioMode=1))

    def addWatermarkToImage(self, image):
        try:
            width, height = image.size

            # 创建一个透明图层，用于添加水印
            txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

            # 获取字体文件的绝对路径
            font_path = os.path.abspath("Rajdhani-Regular.ttf")

            # 选择字体和大小
            fnt = ImageFont.truetype(font_path, 40)
            d = ImageDraw.Draw(txt)

            # 定义水印文本
            text = "LFNL SCIENCE TECHNOLOGY AND CULTURE DIVISION OF EN"

            # 获取文本边界框
            textbbox = d.textbbox((0, 0), text, font=fnt)
            textwidth = textbbox[2] - textbbox[0]
            textheight = textbbox[3] - textbbox[1]

            # 计算文本位置（右下角）
            x = width - textwidth - 10
            y = height - textheight - 20

            # 确定水印颜色
            if self.blackRadio.isChecked():
                text_color = (0, 0, 0, 128)  # 黑色透明
            else:
                text_color = (255, 255, 255, 128)  # 白色透明

            # 绘制水印文本
            d.text((x, y), text, font=fnt, fill=text_color)

            # 合并原始图像和水印图层
            watermarked = Image.alpha_composite(image, txt)
            return watermarked

        except Exception as e:
            # 捕获并打印异常信息
            print(f"An error occurred: {e}")
            return None

    def previewWatermark(self):
        if self.imagePath:
            try:
                # 打开原始图像
                original = Image.open(self.imagePath).convert("RGBA")

                # 添加水印
                self.previewImage = self.addWatermarkToImage(original)

                if self.previewImage:
                    # 将图像从 RGBA 转换为 RGB 并显示
                    preview_rgb = self.previewImage.convert("RGB")
                    preview_path = "preview.jpg"
                    preview_rgb.save(preview_path)

                    # 更新 QLabel 显示预览的带水印的图像
                    qimage = QImage(preview_path)
                    self.label.setPixmap(QPixmap.fromImage(qimage).scaled(self.label.size(), aspectRatioMode=1))

            except Exception as e:
                print(f"An error occurred: {e}")

    def saveWatermark(self):
        if self.previewImage:
            try:
                # 将图像从 RGBA 转换为 RGB 并保存
                self.previewImage = self.previewImage.convert("RGB")

                # 保存到修改后图片目录
                modified_dir = "修改后图片"
                if not os.path.exists(modified_dir):
                    os.makedirs(modified_dir)
                count = len(os.listdir(modified_dir)) + 1
                save_path = os.path.join(modified_dir, f"M_{count:02d}.jpg")
                self.previewImage.save(save_path)

                # 更新 QLabel 显示新的带水印的图像
                qimage = QImage(save_path)
                self.label.setPixmap(QPixmap.fromImage(qimage).scaled(self.label.size(), aspectRatioMode=1))

            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WatermarkApp()
    ex.show()
    sys.exit(app.exec_())
