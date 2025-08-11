from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from controller.controller_gui import ControllerGUI
from view.chat_gui import ChatUI
from view.configuration_gui import ConfigurationUI


class App_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LuminAI")
        self.stacked_widget = QStackedWidget()
        self.controller = ControllerGUI()

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

    def go_to_configuration_screen(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_chat_screen(self):
        self.stacked_widget.setCurrentIndex(0)