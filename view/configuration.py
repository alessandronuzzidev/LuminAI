from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QScrollArea, QLabel
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class ConfigurationUI(QWidget):
    def __init__(self, on_chat_click=None):
        super().__init__()
        self.on_chat_click = on_chat_click
        self.setup_window()
        self.create_interface()
        
    def setup_window(self):
        self.setWindowTitle("LuminAI")
        self.setStyleSheet(self.general_style())
    
    def handle_chat_click(self):
        if self.on_chat_click:
            self.on_chat_click()
    
    def create_interface(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.create_navbar())
        main_layout.addWidget(self.create_content_area(), 1)
        #main_layout.addWidget(self.create_input_area())

        #self.save_button.clicked.connect(self.create_user_message)
    
    def create_navbar(self):
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(20, 10, 20, 10)
        navbar_layout.setSpacing(15)

        image_label = QLabel()
        logo = QIcon("assets/LuminAI.png")
        image_label.setPixmap(logo.pixmap(QSize(150, 50)))
        image_label.setScaledContents(True)
        image_label.setAlignment(Qt.AlignLeft)

        chat_button = QPushButton()
        chat_icon = QIcon("assets/chat.svg")
        chat_button.setIcon(chat_icon)
        chat_button.setIconSize(QSize(24, 24))
        chat_button.setStyleSheet(self.navbar_button_style())
        chat_button.clicked.connect(self.handle_chat_click)

        navbar_layout.addWidget(image_label)
        navbar_layout.addStretch()
        navbar_layout.addWidget(chat_button)

        navbar = QWidget()
        navbar.setLayout(navbar_layout)
        return navbar
    
    def create_content_area(self):
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setStyleSheet(self.scroll_area_style())

        self.chat_container_widget = QWidget()
        self.chat_container_widget.setStyleSheet(self.chat_container_style())

        self.chat_content_layout = QVBoxLayout(self.chat_container_widget)
        self.chat_content_layout.setContentsMargins(20, 20, 20, 20)
        self.chat_content_layout.setSpacing(12)
        self.chat_content_layout.addStretch()

        self.chat_scroll_area.setWidget(self.chat_container_widget)
        return self.chat_scroll_area
    
    # Styles
    def general_style(self):
        return """
            * {
                font-family: 'Helvetica Neue';
                font-size: 15px;
                background-color: #ffffff;
            }
            QWidget {
                background-color: white;
            }
        """

    def navbar_button_style(self):
        return """
            QPushButton {
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c8ead4;
            }
            QPushButton:pressed {
                background-color: #b4dec3;
            }
        """

    def scroll_area_style(self):
        return """
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 0px;
                border-radius: 20px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #555;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """

    def chat_container_style(self):
        return """
            QWidget {
                background-color: #c8ead4;
                border: none;
            }
        """

    def input_style(self):
        return """
            QTextEdit {
                border: 1px solid #e0e0e0;
                padding: 10px 14px;
                border-radius: 8px;
                max-height: 100px;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 5px;
                border-radius: 20px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #555;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c8ead4;
            }
            QPushButton:pressed {
                background-color: #b4dec3;
            }
        """