from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidget, QLineEdit, QFileDialog
import os
from PIL import Image, ImageOps, ImageFilter
from PyQt5.QtGui import QPixmap

workdir = ''
# MKDIR (Создать Директорию): MK - Make, DIR - Directory

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.save_dir = 'Modified/'

    def loadImage(self, filename):
        self.filename = filename
        self.dir = workdir
        image_path = os.path.join(self.dir, self.filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        pixmapimage = QPixmap(path) 
        label_width, label_height = Picture.width(), Picture.height() 
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio) 
        Picture.setPixmap(scaled_pixmap) 
        Picture.setVisible(True)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = ImageOps.grayscale(self.image)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.rotate(-90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage(): # Показывает Выбранную Картинку
    if Pic_List.currentRow() >= 0:
        filename = Pic_List.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, filename) # Путь до *Файла*
        workimage.showImage(image_path)

def chooseWorkdir():
    global workdir
    workdir = QFileDialog().getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
                break
    return result  

def showFilenamesList(): # Список файлов
    chooseWorkdir()
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.jfif', '.bmp']
    files = os.listdir(workdir)
    files = filter(files, extensions)
    Pic_List.clear()
    Pic_List.addItems(files)


app = QApplication([]) # приложение
window = QWidget() # окно
window.setWindowTitle('TheRedacted Ω')
window.resize(700, 500)

# ----------------------------------------

Picture = QLabel('картинка')
Pic_List = QListWidget()
Button_Folder = QPushButton('Папка')
Button_LeftRotate = QPushButton('<- 90*')
Button_RightRotate = QPushButton('-> 90*')
Button_Mirror = QPushButton('Отзеркалить')
Button_Sharpen = QPushButton('Резкость')
Button_BlackWhite = QPushButton('Ч/Б')

# ----------------------------------------

gH_Line1 = QHBoxLayout()
H_Line2 = QHBoxLayout()
V_Line1 = QVBoxLayout()
V_Line2 = QVBoxLayout()

V_Line1.addWidget(Button_Folder)
V_Line1.addWidget(Pic_List)
V_Line2.addWidget(Picture)
H_Line2.addWidget(Button_LeftRotate)
H_Line2.addWidget(Button_RightRotate)
H_Line2.addWidget(Button_Mirror)
H_Line2.addWidget(Button_Sharpen)
H_Line2.addWidget(Button_BlackWhite)

V_Line2.addLayout(H_Line2)
gH_Line1.addLayout(V_Line1)
gH_Line1.addLayout(V_Line2)
window.setLayout(gH_Line1)

# ----------------------------------------

Button_Folder.clicked.connect(showFilenamesList)
Pic_List.currentRowChanged.connect(showChosenImage)
Button_BlackWhite.clicked.connect(workimage.do_bw)
Button_LeftRotate.clicked.connect(workimage.do_left)
Button_RightRotate.clicked.connect(workimage.do_right)
Button_Mirror.clicked.connect(workimage.do_mirror)
Button_Sharpen.clicked.connect(workimage.do_sharpen)

# ----------------------------------------

window.show() #показать окно
app.exec() #открыть окно