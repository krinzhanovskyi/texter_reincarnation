import sys
import time
import random
import threading
import pyperclip
import keyboard
import ctypes
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QSlider
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QObject

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class WorkerSignals(QObject):
    update_status = pyqtSignal(str)
    finished = pyqtSignal()

class AutoTyperApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Threading event used for instant interruption of the typing process
        self.stop_event = threading.Event()
        self.current_speed = 20 # Default speed in characters per second

        # Connect signals to UI update methods
        self.signals = WorkerSignals()
        self.signals.update_status.connect(self.set_status)
        self.signals.finished.connect(lambda: self.btn_start.setEnabled(True))

        self.initUI()
        
        # Register global hotkey that works even when the app is minimized
        keyboard.add_hotkey('f12', self.panic)

    def initUI(self):
        self.setWindowTitle('Texter Reincarnation')
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        self.resize(400, 380)
        
        # Keep the application window always on top of other windows (e.g., browser)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()

        # Text preview and editing area
        self.text_preview = QTextEdit()
        layout.addWidget(self.text_preview)

        # Speed adjustment slider (1 to 50 chars/sec)
        self.lbl_speed = QLabel(f'Speed: {self.current_speed} chars/s')
        layout.addWidget(self.lbl_speed)

        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setMinimum(1)
        self.slider_speed.setMaximum(50)
        self.slider_speed.setValue(self.current_speed)
        self.slider_speed.valueChanged.connect(self.update_speed_label)
        layout.addWidget(self.slider_speed)

        self.btn_load = QPushButton('Upload from Clipboard')
        self.btn_load.clicked.connect(self.load_clipboard)
        layout.addWidget(self.btn_load)

        self.btn_start = QPushButton('Start Typing')
        self.btn_start.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_start.clicked.connect(self.start_typing)
        layout.addWidget(self.btn_start)

        self.lbl_status = QLabel('Ready')
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_status)

        self.setLayout(layout)
        self.load_clipboard()

    def update_speed_label(self, value):
        self.current_speed = value
        self.lbl_speed.setText(f'Speed: {self.current_speed} chars/s')

    def load_clipboard(self):
        self.text_preview.setPlainText(pyperclip.paste())
        self.set_status("I'm ready to work.")

    def set_status(self, text):
        self.lbl_status.setText(text)

    def panic(self):
        # Trigger the event to immediately break the typing loop
        self.stop_event.set()
        self.signals.update_status.emit('STOPPED (F12)')

    def start_typing(self):
        text = self.text_preview.toPlainText()
        if not text:
            return

        # Reset the stop event for a new typing session and lock the start button
        self.stop_event = threading.Event()
        self.btn_start.setEnabled(False)

        # Launch the typing process in a background thread to prevent GUI freezing
        threading.Thread(target=self._type_worker, args=(text, self.stop_event), daemon=True).start()

    def _type_worker(self, text, stop):
        try:
            # 5-second delay allowing the user to focus the target window
            for i in range(5, 0, -1):
                self.signals.update_status.emit(f'Start in {i}...')
                if stop.wait(1): # Interrupts if panic button is pressed during countdown
                    return

            self.signals.update_status.emit('Start working. F12 to STOP')

            for char in text:
                if stop.is_set():
                    return

                # Simulate physical 'Enter' key press for actual line breaks
                if char == '\n':
                    keyboard.send('enter')
                else:
                    keyboard.write(char)

                # Humanization logic: add +/- 20% random variance to the typing speed
                base = 1 / self.current_speed
                if stop.wait(random.uniform(base * 0.8, base * 1.2)):
                    return

            self.signals.update_status.emit('Done!')
        finally:
            # Ensures the Start button is always unlocked, regardless of success or forced stop
            self.signals.finished.emit()

    def closeEvent(self, e):
        """
        Cleanup method called when the application window is closed.
        Prevents background processes and global hotkeys from hanging in OS memory.
        """
        self.stop_event.set()
        keyboard.unhook_all()
        super().closeEvent(e)


if __name__ == '__main__':
    # Set a custom Application User Model ID for Windows
    # This ensures the custom icon is displayed on the taskbar instead of the default Python logo
    myappid = 'my_custom_autotyper_v2' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    window = AutoTyperApp()
    window.show()
    sys.exit(app.exec())