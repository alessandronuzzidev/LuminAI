from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QScrollArea, QLabel
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPalette, QColor


class ChatUI(QWidget):
    def __init__(self, on_config_click=None):
        super().__init__()
        self.on_config_click = on_config_click
        self.setup_window()
        self.create_interface()

    def setup_window(self):
        self.setWindowTitle("LuminAI")
        self.setStyleSheet(self.general_style())

    def create_user_message(self): 
        text = self.input_text.toPlainText().strip()
        if not text:
            return

        message = QLabel(text.replace('\n', '<br>'))
        message.setWordWrap(True)
        message.setTextFormat(Qt.RichText)
        message.setStyleSheet(self.user_message_style())

        self.chat_content_layout.insertWidget(
            self.chat_content_layout.count() - 1, message, 0
        )

        self.input_text.clear()
        self.input_text.setFocus()
        self.chat_container_widget.adjustSize()

        QApplication.processEvents()
        self.chat_scroll_area.verticalScrollBar().setValue(
            self.chat_scroll_area.verticalScrollBar().maximum()
        )
        
    def handle_config_click(self):
        if self.on_config_click:
            self.on_config_click()


    def create_interface(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.create_navbar())
        main_layout.addWidget(self.create_chat_area(), 1)
        main_layout.addWidget(self.create_input_area())

        self.send_button.clicked.connect(self.create_user_message)

    def create_navbar(self):
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(20, 10, 20, 10)
        navbar_layout.setSpacing(15)

        image_label = QLabel()
        logo = QIcon("assets/LuminAI.png")
        image_label.setPixmap(logo.pixmap(QSize(150, 50)))
        image_label.setScaledContents(True)
        image_label.setAlignment(Qt.AlignLeft)
        
        reset_button = QPushButton()
        reset_icon = QIcon("assets/reset.svg")
        reset_button.setIcon(reset_icon)
        reset_button.setIconSize(QSize(24, 24))
        reset_button.setStyleSheet(self.navbar_button_style())
        #reset_button.clicked.connect(self.create_user_message)

        config_button = QPushButton()
        config_icon = QIcon("assets/config_final.svg")
        config_button.setIcon(config_icon)
        config_button.setIconSize(QSize(24, 24))
        config_button.setStyleSheet(self.navbar_button_style())
        config_button.clicked.connect(self.handle_config_click)

        navbar_layout.addWidget(image_label)
        navbar_layout.addStretch()
        
        navbar_layout.addWidget(reset_button)
        navbar_layout.addWidget(config_button)

        navbar = QWidget()
        navbar.setLayout(navbar_layout)
        return navbar

    def create_chat_area(self):
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

    def create_input_area(self):
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(20, 20, 20, 20)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Escribe un mensaje...")
        self.input_text.setFixedHeight(40)
        palette = self.input_text.palette()
        palette.setColor(QPalette.PlaceholderText, QColor("#a1a1a1"))
        self.input_text.setPalette(palette)
        self.input_text.setStyleSheet(self.input_style())
        input_layout.addWidget(self.input_text)

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(5)

        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(40, 40)
        self.send_button.setStyleSheet(self.button_style())
        buttons_layout.addWidget(self.send_button)

        self.microphone_button = QPushButton()
        self.microphone_button.setIcon(QIcon("assets/microphone_final.svg"))
        self.microphone_button.setIconSize(QSize(24, 24))
        self.microphone_button.setFixedSize(40, 40)
        self.microphone_button.setStyleSheet(self.button_style())
        buttons_layout.addWidget(self.microphone_button)

        input_layout.addLayout(buttons_layout)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        input_widget.setStyleSheet("background-color: #ffffff;")
        return input_widget

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

    def user_message_style(self):
        return """
            background-color: #c8ead4;
            border-radius: 12px;
            padding: 20px 20px;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 15px;
            color: #202123;
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
                background-color: white;
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