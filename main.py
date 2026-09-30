import sys
import time
import random
import threading
import pyperclip
import keyboard
import ctypes
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QIcon

class WorkerSignals(QObject):
    update_status = pyqtSignal(str)

class AutoTyperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.stop_typing = False
        
        self.signals = WorkerSignals()
        self.signals.update_status.connect(self.set_status)
        
        self.initUI()
        
        # Stop buttom
        keyboard.add_hotkey('f12', self.panic)

    def initUI(self):
        self.setWindowTitle('TEXTER BY REINCARNATION')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(400, 300)
        # 1st project window
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        
        # preview
        self.text_preview = QTextEdit()
        layout.addWidget(self.text_preview)

        # buttons
        self.btn_load = QPushButton('Update')
        self.btn_load.clicked.connect(self.load_clipboard)
        layout.addWidget(self.btn_load)

        self.btn_start = QPushButton('Start')
        self.btn_start.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_start.clicked.connect(self.start_typing)
        layout.addWidget(self.btn_start)

        # status of programm
        self.lbl_status = QLabel('Ready. To stop: F12')
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_status)

        self.setLayout(layout)
        self.load_clipboard()

    def load_clipboard(self):
        self.text_preview.setPlainText(pyperclip.paste())
        self.set_status("Text is here. im ready")

    def set_status(self, text):
        self.lbl_status.setText(text)

    def panic(self):
        self.stop_typing = True
        self.signals.update_status.emit('🛑 STOPPED! (F12)')

    def start_typing(self):
        text = self.text_preview.toPlainText()
        if not text:
            return
            
        self.stop_typing = False
        self.btn_start.setEnabled(False)
        threading.Thread(target=self._type_worker, args=(text,), daemon=True).start()

    def _type_worker(self, text):
        # 3 seks time
        for i in range(3, 0, -1):
            if self.stop_typing: 
                self._finish_worker()
                return
            self.signals.update_status.emit(f'You have time to find where should i work ! Start in {i}...')
            time.sleep(1)
        
        self.signals.update_status.emit('⌨ On working... (F12 to stop)')
        
        # texing
        for char in text:
            if self.stop_typing:
                self._finish_worker()
                return
            keyboard.write(char)
            time.sleep(random.uniform(0.02, 0.05))
        
        if not self.stop_typing:
            self.signals.update_status.emit('Done!')
        
        self._finish_worker()

    def _finish_worker(self):
        self.btn_start.setEnabled(True)

if __name__ == '__main__':
    myappid = 'my_custom_autotyper_v1' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = QApplication(sys.argv)
    window = AutoTyperApp()
    window.show()
    sys.exit(app.exec())