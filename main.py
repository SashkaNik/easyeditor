from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import os

app = QApplication([])
win = QWidget()
win.setWindowTitle('Easy Editor')
win.resize(700, 500)

btn_dir = QPushButton('Folder')
elements = QListWidget()
kartinka = QLabel('Picture')
btn_left = QPushButton('Left')
btn_right = QPushButton('Right')
btn_mirror = QPushButton('Mirror')
btn_contrast = QPushButton('Sharpness')
btn_blur = QPushButton('Blur')
btn_bw = QPushButton('B/w')
btn_save = QPushButton('Save')
btn_reset = QPushButton('Reset')

row = QHBoxLayout()
row_tools = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(elements)
col2.addWidget(kartinka, 95)
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_contrast)
row_tools.addWidget(btn_blur)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_save)
row_tools.addWidget(btn_reset)

col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 88)


workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    try:
        filenames = filter(os.listdir(workdir), extensions)
        elements.clear()
        for filename in filenames:
            elements.addItem(filename)
    except:
        pass


class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.save_dir = 'Modified/'
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = kartinka.width(), kartinka.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        kartinka.setPixmap(scaled_pixmap)
        kartinka.setVisible(True)
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.rotate(-90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_contrast(self):
        self.image =  ImageEnhance.Contrast(self.image).enhance(1.5)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_blur(self):
        self.image =  self.image.filter(ImageFilter.GaussianBlur(10))
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if elements.currentRow() >= 0:
        filename = elements.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)


elements.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_contrast.clicked.connect(workimage.do_contrast)
btn_blur.clicked.connect(workimage.do_blur)
btn_save.clicked.connect(workimage.saveImage)
btn_reset.clicked.connect(showChosenImage)
btn_dir.clicked.connect(showFilenamesList)
btn_save.clicked.connect(workimage.saveImage)

win.setLayout(row)
win.show()
app.exec()
