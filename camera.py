import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Camera")
        # self.resize(1280, 720)
        self.CAMERA_INDEX = 0

        self.camera = cv2.VideoCapture(self.CAMERA_INDEX)



        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setScaledContents(True)

        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        self.setLayout(layout)


        self.take_pic_btn = QPushButton("Capture")
        layout.addWidget(self.take_pic_btn)

        self.take_pic_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 40px;
                background-color: hsl(12, 96%, 58%);
                font-size: 24px;
                font-family: Arial;
                color: white;
                border-radius: 10px;
                border: none;
                cursor: pointer;
            }

            QPushButton:hover {
                background-color: hsl(12, 96%, 68%);
            }

            QPushButton:pressed {
                background-color: hsl(12, 96%, 78%);
            }
        """)

        self.take_pic_btn.setCursor(Qt.PointingHandCursor)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.take_pic_btn.clicked.connect(self.capture_image)

    def update_frame(self):
        success, frame = self.camera.read()
        if not success:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = frame.shape
        bytes_per_line = channels * width

        image = QImage(
            frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888,
        )
        self.camera_label.setPixmap(QPixmap.fromImage(image.copy()))


    def capture_image(self):
        success, frame = self.camera.read()
        if not success:
            print("Failed to capture image")
            return
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_name = f"QT-CAPTURE-{current_datetime}.jpg"
        file_path = f"captured-images/{image_name}"
        cv2.imwrite(file_path, frame)

        print("Image saved successfully!")


app = QApplication(sys.argv)
window = CameraWindow()
window.show()
sys.exit(app.exec_())
