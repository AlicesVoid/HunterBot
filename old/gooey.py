import game
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main layout
        main_layout = QVBoxLayout()

        # 1. Display the images side by side
        image_layout = QHBoxLayout()
        pixmap = QPixmap('src/blank.png')

        for _ in range(2):
            label = QLabel()

            # Calculate the scaled size while maintaining the aspect ratio
            scaled_size = pixmap.size()
            scaled_size.scale(label.size(), Qt.KeepAspectRatio)

            label.setPixmap(pixmap.scaled(scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setAlignment(Qt.AlignCenter)  # Center the image in case the label's size is larger

            image_layout.addWidget(label)

        main_layout.addLayout(image_layout)

        # 2. Add a divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(divider)

        # 3. Add a Text Box for Display Purposes 
        text_label = QLabel("PissFart")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("QLabel { max-height: 3em; text-overflow: ellipsis; }")
        main_layout.addWidget(text_label)
        

        # 4. Add a divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(divider)

        # 5. Add three buttons
        button_layout = QHBoxLayout()
        for name in ['start', 'middle', 'exit']:
            btn = QPushButton(name)
            button_layout.addWidget(btn)
        main_layout.addLayout(button_layout)

        # Set up the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set the window properties
        self.setWindowTitle('Image and Buttons GUI')
        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())




