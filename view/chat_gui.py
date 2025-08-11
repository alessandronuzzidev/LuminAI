from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QScrollArea, QLabel
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon, QPalette, QColor


from PySide6.QtCore import QThread, Signal, QObject

class LLMWorker(QObject):
    finished = Signal(str)

    def __init__(self, text, llm_function):
        super().__init__()
        self.text = text
        self.llm_function = llm_function

    def run(self):
        response = self.llm_function(self.text)
        self.finished.emit(response)



class ChatUI(QWidget):
    def __init__(self, on_config_click=None, controller=None):
        super().__init__()
        self.on_config_click = on_config_click
        self.controller = controller
        self.setup_window()
        self.create_interface()

    def setup_window(self):
        self.setWindowTitle("LuminAI")
        self.setStyleSheet(self.general_style())
        
    def create_llm_message(self, text):
        message = QLabel(text.replace('\n', '<br>'))
        message.setWordWrap(True)
        message.setTextFormat(Qt.RichText)
        message.setStyleSheet(self.llm_message_style())

        self.chat_content_layout.insertWidget(
            self.chat_content_layout.count() - 1, message, 0
        )
        
        self.chat_container_widget.adjustSize()
        self.chat_scroll_area.verticalScrollBar().setValue(
            self.chat_scroll_area.verticalScrollBar().maximum()
        )
        
    def show_llm_response(self, answer):
        if hasattr(self, "loading_label") and self.loading_label:
            self.chat_content_layout.removeWidget(self.loading_label)
            self.loading_label.deleteLater()
            self.loading_label = None

        self.create_llm_message(answer)
        self.send_button.setEnabled(True) 
    
    def call_llm_and_update(self, text):
        answer = self.controller.send_message_to_llm(text)

        QTimer.singleShot(0, lambda: self.show_llm_response(answer))
        
    def scroll_to_bottom(self):
        QApplication.processEvents()
        self.chat_scroll_area.verticalScrollBar().setValue(
            self.chat_scroll_area.verticalScrollBar().maximum()
        )
       
    def create_user_message(self): 
        text = self.input_text.toPlainText().strip()
        if not text:
            return

        user_message = QLabel(text.replace('\n', '<br>'))
        user_message.setWordWrap(True)
        user_message.setTextFormat(Qt.RichText)
        user_message.setStyleSheet(self.user_message_style())
        self.chat_content_layout.insertWidget(self.chat_content_layout.count() - 1, user_message, 0)

        self.loading_label = QLabel("Pensando...")
        self.loading_label.setWordWrap(True)
        self.loading_label.setTextFormat(Qt.RichText)
        self.loading_label.setStyleSheet("font-style: italic; color: #999; padding: 20px;")
        self.chat_content_layout.insertWidget(self.chat_content_layout.count() - 1, self.loading_label, 0)

        self.input_text.clear()
        self.input_text.setFocus()
        self.chat_container_widget.adjustSize()
        self.scroll_to_bottom()

        self.send_button.setEnabled(False)
        self.thread = QThread()
        self.worker = LLMWorker(text, self.controller.send_message)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.show_llm_response)
        self.worker.finished.connect(self.scroll_to_bottom)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        
    def restart_chat(self):
        self.controller.restart_chat()
        while self.chat_content_layout.count() > 0:
            item = self.chat_content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        self.chat_content_layout.addStretch()
        
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
        self.reset_button.clicked.connect(self.restart_chat)

    def create_navbar(self):
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(20, 10, 20, 10)
        navbar_layout.setSpacing(15)

        image_label = QLabel()
        logo = QIcon("assets/LuminAI.png")
        image_label.setPixmap(logo.pixmap(QSize(150, 50)))
        image_label.setScaledContents(True)
        image_label.setAlignment(Qt.AlignLeft)
        
        self.reset_button = QPushButton()
        reset_icon = QIcon("assets/reset.svg")
        self.reset_button.setIcon(reset_icon)
        self.reset_button.setIconSize(QSize(24, 24))
        self.reset_button.setStyleSheet(self.navbar_button_style())
        self.reset_button.setCursor(Qt.PointingHandCursor)
        #reset_button.clicked.connect(self.create_user_message)

        config_button = QPushButton()
        config_icon = QIcon("assets/config_final.svg")
        config_button.setIcon(config_icon)
        config_button.setIconSize(QSize(24, 24))
        config_button.setStyleSheet(self.navbar_button_style())
        config_button.setCursor(Qt.PointingHandCursor)
        config_button.clicked.connect(self.handle_config_click)

        navbar_layout.addWidget(image_label)
        navbar_layout.addStretch()
        
        navbar_layout.addWidget(self.reset_button)
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
        self.send_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(self.send_button)

        self.microphone_button = QPushButton()
        self.microphone_button.setIcon(QIcon("assets/microphone_final.svg"))
        self.microphone_button.setIconSize(QSize(24, 24))
        self.microphone_button.setFixedSize(40, 40)
        self.microphone_button.setStyleSheet(self.button_style())
        #buttons_layout.addWidget(self.microphone_button)

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
        
    def llm_message_style(self):
        return """
            background-color: white;
            border-radius: 12px;
            padding: 20px 20px;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 15px;
            color: black;
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