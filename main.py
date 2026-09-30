import sys
import time
import random
import threading
import pyperclip
import keyboard
import ctypes
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QSlider
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QObject

class WorkerSignals(QObject):
    update_status = pyqtSignal(str)

class AutoTyperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.stop_typing = False
        self.current_speed = 0.05 
        
        self.signals = WorkerSignals()
        self.signals.update_status.connect(self.set_status)
        
        self.initUI()
        
        # global panic button
        keyboard.add_hotkey('f12', self.panic)

    def initUI(self):
        self.setWindowTitle('Texter Reincarnation')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(400, 380)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        
        self.text_preview = QTextEdit()
        layout.addWidget(self.text_preview)

        # speed slider setup
        self.lbl_speed = QLabel(f'Speed: {self.current_speed:.2f} letters/seconds')
        layout.addWidget(self.lbl_speed)

        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setMinimum(1)
        self.slider_speed.setMaximum(100)
        self.slider_speed.setValue(5)
        self.slider_speed.valueChanged.connect(self.update_speed_label)
        layout.addWidget(self.slider_speed)

        # buttons
        self.btn_load = QPushButton('Upload')
        self.btn_load.clicked.connect(self.load_clipboard)
        layout.addWidget(self.btn_load)

        self.btn_start = QPushButton('Start')
        self.btn_start.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_start.clicked.connect(self.start_typing)
        layout.addWidget(self.btn_start)

        # status label
        self.lbl_status = QLabel('Ready')
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_status)

        self.setLayout(layout)
        self.load_clipboard()

    def update_speed_label(self, value):
        self.current_speed = value / 100.0
        self.lbl_speed.setText(f'Speed: {self.current_speed:.2f} letters/seconds')

    def load_clipboard(self):
        self.text_preview.setPlainText(pyperclip.paste())
        self.set_status("Im ready to work.")

    def set_status(self, text):
        self.lbl_status.setText(text)

    def panic(self):
        self.stop_typing = True
        self.signals.update_status.emit('STOPPED (F12)')

    def start_typing(self):
        text = self.text_preview.toPlainText()
        if not text:
            return
            
        self.stop_typing = False
        self.btn_start.setEnabled(False)
        
        threading.Thread(target=self._type_worker, args=(text,), daemon=True).start()

    def _type_worker(self, text):
        for i in range(5, 0, -1):
            if self.stop_typing: 
                self._finish_worker()
                return
            self.signals.update_status.emit(f'Start in {i}...')
            time.sleep(1)
        
        self.signals.update_status.emit('Start working. F12 to STOP')

        for char in text:
            if self.stop_typing:
                self._finish_worker()
                return
            
            # check for our special enter trigger
            if char == '<':
                keyboard.send('enter')
            else:
                keyboard.write(char)
                
            #humanisation
            human_delay = random.uniform(self.current_speed * 0.8, self.current_speed * 1.2)
            time.sleep(human_delay)
        
        if not self.stop_typing:
            self.signals.update_status.emit('Done!')
        
        self._finish_worker()

    def _finish_worker(self):
        self.btn_start.setEnabled(True)


if __name__ == '__main__':
    myappid = 'my_custom_autotyper_v2' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = QApplication(sys.argv)
    window = AutoTyperApp()
    window.show()
    sys.exit(app.exec())