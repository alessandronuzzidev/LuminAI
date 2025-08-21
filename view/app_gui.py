from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QProgressDialog
from PySide6.QtCore import QTimer, Qt
from controller.controller import Controller
from view.chat_gui import ChatUI
from view.configuration_gui import ConfigurationUI

from services.control_monitor_lib import control_monitor

class App_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LuminAI")
        self.stacked_widget = QStackedWidget()
        self.controller = Controller()
        
        current, total = self.controller.get_progress()
        if current or total:
            self.progress_dialog = QProgressDialog("Indexando archivos...", "Cancelar", 0, total, self)
            self.progress_dialog.setWindowTitle("Indexando...")
            self.progress_dialog.setWindowModality(Qt.ApplicationModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setValue(current)
            self.progress_dialog.canceled.connect(self.cancel_indexing)

            self.progress_timer = QTimer()
            self.progress_timer.timeout.connect(self.update_progress_from_manager)
            self.progress_timer.start(1000) 
        
        control_monitor("pause")

        self.chat = ChatUI(self.go_to_configuration_screen, self.controller)
        self.configuration = ConfigurationUI(self.go_to_chat_screen, self.controller)

        self.stacked_widget.addWidget(self.chat)
        self.stacked_widget.addWidget(self.configuration)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.setMinimumSize(1100, 720)
        self.resize(1100, 720)
        
    def update_progress_from_manager(self):
        current, total = self.controller.get_progress()
        if current is None or total is None:
            return
        self.progress_dialog.setMaximum(total)
        self.progress_dialog.setValue(current)
        self.progress_dialog.setLabelText(f"Indexando archivos...\nDocumentos procesados: {current} / {total}")

        if current >= total:
            self.progress_timer.stop()
            self.progress_dialog.close()
            
    def cancel_indexing(self):
        self.controller.cancel_indexing()
        self.progress_timer.stop()
        self.progress_dialog.close()

    def go_to_configuration_screen(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_chat_screen(self):
        self.stacked_widget.setCurrentIndex(0)