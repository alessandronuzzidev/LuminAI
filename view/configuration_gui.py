from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFrame, QFileDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class ConfigurationUI(QWidget):
    def __init__(self, on_chat_click=None, controller=None):
        super().__init__()
        self.on_chat_click = on_chat_click
        self.controller = controller
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
    
    def select_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecciona una carpeta")
        if folder:
            self.path_input.setText(folder)
            
    def handle_path_input(self):
        path = self.path_input.text()
        model = "Ollama 3.2"
        self.controller.init_charge_documents(path, model)
            
    def add_path_input(self, content_layout):
        path_info = QLabel("Especifica la carpeta donde se encuentran los documentos que deseas consultar.")
        path_info.setStyleSheet(self.text_style())
        path_info.setWordWrap(True)

        content_layout.addWidget(path_info)

        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Selecciona la carpeta...")
        self.path_input.setText(self.controller.get_path())
        self.path_input.setStyleSheet(self.input_style())
        
        path_button = QPushButton("Explorador de archivos")
        path_button.setFixedSize(180, 40)
        path_button.clicked.connect(self.select_dir)
        path_button.setStyleSheet(self.finder_button_style())
        
        load_button = QPushButton("Iniciar carga de documentos")
        load_button.setFixedSize(220, 40)
        load_button.setStyleSheet(self.init_charge_button_style())

        load_button.clicked.connect(self.handle_path_input)

        path_layout.addWidget(self.path_input)
        path_layout.addWidget(path_button)
        path_layout.addWidget(load_button)

        content_layout.addLayout(path_layout)

            
    def add_models(self, content_layout):
        model_info = QLabel("Elige el modelo de embedding a utilizar para recuperar y entender la información de tus documentos.")
        model_info.setStyleSheet(self.text_style())
        model_info.setWordWrap(True)
        
        content_layout.addWidget(model_info)

        model_card = QFrame()
        model_card.setFrameShape(QFrame.StyledPanel)
        model_card.setStyleSheet("""
            QFrame {
                background-color: #f7f7f7;
                border-radius: 12px;
                border: 1px solid #dcdcdc;
            }
        """)
        
        model_layout = QVBoxLayout(model_card)
        model_layout.setContentsMargins(20, 20, 20, 20)
        model_layout.setSpacing(10)

        model_name = QLabel("Modelo: Ollama 3.2")
        model_name.setStyleSheet("font-size: 16px; font-weight: bold;")

        specs = QLabel(
            "• Tamaño: 7B\n"
            "• Velocidad: Alta\n"
            "• Compatible: Sí\n"
            "• Tipo: LLM local\n"
            "• Framework: Ollama\n"
            "• Lenguaje: Multilingüe"
        )
        specs.setStyleSheet("font-size: 14px;")

    
    def create_content_area(self):
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignTop) 

        self.add_path_input(content_layout)
        self.add_models(content_layout)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        return content_widget
    
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
        
    def text_style(self):
        return """
            QLabel {
                font-size: 14px; 
                color: #444;
            }
        """
        
    def input_style(self):
        return """
            QLineEdit {
                padding: 8px; 
                border-radius: 8px; 
                border: 1px solid #ccc;
            }
        """
        
    def finder_button_style(self):
        return """
            QPushButton {
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                background-color: #e0e0e0;
            }
            QPushButton:hover {
                background-color: #c8ead4;
            }
            QPushButton:pressed {
                background-color: #b4dec3;
            }
        """
        
    def init_charge_button_style(self):
        return """
            QPushButton {
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                background-color: #e0e0e0;
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
