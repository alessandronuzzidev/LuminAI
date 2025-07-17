import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QScrollArea, QLabel
)
from PySide6.QtCore import (Qt, QSize)
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPalette, QColor


class LuminAIChatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LuminAI")
        self.setMinimumSize(900, 600)
        self.resize(1100, 720)
        self.setStyleSheet(self.general_style())
        self.create_interface()
        
    def create_user_message(self): 
        text = self.input_text.toPlainText().strip()
        if text:

            mark_up = QLabel(text.replace('\n', '<br>'))
            mark_up.setWordWrap(True)
            mark_up.setTextFormat(Qt.RichText)  # Recognition for <br>
            mark_up.setStyleSheet("""
                background-color: #c8ead4;
                border-radius: 12px;
                padding: 20px 20px;
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 15px;
                color: #202123;
            """)

            # Adding to message layout
            self.chat_content_layout.insertWidget(
                self.chat_content_layout.count() - 1, mark_up, 0
            )

            self.input_text.clear()
            self.input_text.setFocus()
            
            self.chat_container_widget.adjustSize()
            
            # Scroll to the bottom
            QApplication.processEvents()
            self.chat_scroll_area.verticalScrollBar().setValue(
                self.chat_scroll_area.verticalScrollBar().maximum()
            )
                        


    def create_interface(self):
        principal_layout = QVBoxLayout(self)
        principal_layout.setContentsMargins(0, 0, 0, 0)
        principal_layout.setSpacing(0)

        # Navbar
        navbar = QHBoxLayout()
        navbar.setContentsMargins(20, 0, 20, 0)
        navbar.setSpacing(15)
        
        image_label = QLabel()
        logo = QIcon("/Users/alessandronuzziherrero/TFM pruebas/Prueba PySide6/assets/LuminAI.png")  # Relative path to logo
        image_label.setPixmap(logo.pixmap(QSize(300, 100)))
        image_label.setScaledContents(True)
        image_label.setAlignment(Qt.AlignLeft)
        

        button_config = QPushButton()
        icon_svg = QIcon("/Users/alessandronuzziherrero/TFM pruebas/Prueba PySide6/assets/config_final.svg")  # Relative path to icon
        button_config.setIcon(icon_svg)
        button_config.setIconSize(QSize(24, 24))
        button_config.setStyleSheet(self.navbar_button_style())
        button_config.setLayoutDirection(Qt.RightToLeft)

        navbar.addWidget(image_label)
        navbar.addStretch()
        navbar.addWidget(button_config)

        navbar_widget = QWidget()
        navbar_widget.setLayout(navbar)
        principal_layout.addWidget(navbar_widget)


        # Conversation (scroll area)
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setStyleSheet(self.scroll_area())
        self.chat_scroll_area.setStyleSheet("""
            border: none;
            background-color: #ffffff;
        """)

        # Chat container widget
        self.chat_container_widget = QWidget()
        self.chat_container_widget.setStyleSheet(self.estilo_chat())
        self.chat_content_layout = QVBoxLayout(self.chat_container_widget)
        self.chat_content_layout.setContentsMargins(20, 20, 20, 20)
        self.chat_content_layout.setSpacing(12)
        self.chat_content_layout.addStretch()
        self.chat_scroll_area.setWidget(self.chat_container_widget)
        principal_layout.addWidget(self.chat_scroll_area, 1)

       # Input area
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
        self.microphone_button.setIcon(QIcon("/Users/alessandronuzziherrero/TFM pruebas/Prueba PySide6/assets/microphone_final.svg"))  # Ruta correcta
        self.microphone_button.setIconSize(QSize(24, 24))
        self.microphone_button.setFixedSize(40, 40)
        self.microphone_button.setStyleSheet(self.button_style())
        buttons_layout.addWidget(self.microphone_button)
        input_layout.addLayout(buttons_layout)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        input_widget.setStyleSheet("background-color: #ffffff;")
        principal_layout.addWidget(input_widget)

        
        self.send_button.clicked.connect(self.create_user_message)


    def general_style(self):
        return """
            * {
                font-family: 'Helvetica Neue';
                font-size: 15px;
                background-color: #ffffff;
            }
            QWidget {
                background-color: #ffffff;
            }
        """
        
    def title(self):
        return """
            QLabel {
                width: 240px;
                height: 120px;
                color: #202123;
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
        
    def scroll_area(self):
        return """
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 5px;
                margin: 0px 0px 0px 0px;
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
                height: 0px; /* Ocultar los botones de arriba y abajo */
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """

    def estilo_chat(self):
        return """
            QWidget {
                background-color: white;
                border: none;

                color: #202123;
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
                margin: 0px 0px 0px 0px;
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
                height: 0px; /* Ocultar los botones de arriba y abajo */
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LuminAIChatUI()
    ventana.show()
    sys.exit(app.exec())
