from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFrame, QFileDialog, QCheckBox, 
    QMessageBox, QRadioButton, QButtonGroup, QProgressDialog
)

from PySide6.QtCore import Qt, QSize, QThread
from PySide6.QtGui import QIcon


class ConfigurationUI(QWidget):
    def __init__(self, on_chat_click=None, controller=None):
        super().__init__()
        self.on_chat_click = on_chat_click
        self.controller = controller
        self.old_config = self.controller.load_config_file()
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
        chat_button.setCursor(Qt.PointingHandCursor)
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
            
    def update_progress(self, current, total):
        if self.progress_dialog:
            self.progress_dialog.setMaximum(total)
            self.progress_dialog.setValue(current)
            self.progress_dialog.setLabelText(f"Indexando archivos...\nDocumentos procesados: {current} / {total}")

    def handle_path_input(self):
        path = self.path_input.text()
        if path != self.old_config["path"]:
            self.controller.update_path(path)
            self.old_config = self.controller.load_config_file()

            self.progress_dialog = QProgressDialog("Indexando archivos...", "Cancelar", 0, 0, self)
            self.progress_dialog.setWindowTitle("Indexando")
            self.progress_dialog.setWindowModality(Qt.ApplicationModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setValue(0)
            self.progress_dialog.show()

            self.controller.thread_function(update_function=self.update_progress, progress_dialog=self.progress_dialog)
        else:
            print("Same dir!!!")

            
    def add_path_input(self, content_layout):
        title = QLabel("Configuración de ruta de documentos")
        title.setStyleSheet(self.title_style())
        content_layout.addWidget(title)
        
        padded_container = QWidget()
        padded_layout = QVBoxLayout()
        padded_layout.setContentsMargins(10, 0, 10, 0)
        padded_container.setLayout(padded_layout)

        path_info = QLabel("Especifica la carpeta donde se encuentran los documentos que deseas consultar.")
        path_info.setStyleSheet(self.text_style())
        path_info.setWordWrap(True)
        padded_layout.addWidget(path_info)

        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Selecciona la carpeta...")
        self.path_input.setText(self.old_config["path"])
        self.path_input.setStyleSheet(self.input_style())
        
        path_button = QPushButton("Explorador de archivos")
        path_button.setFixedSize(180, 40)
        path_button.clicked.connect(self.select_dir)
        path_button.setCursor(Qt.PointingHandCursor)
        path_button.setStyleSheet(self.finder_button_style())
        
        load_button = QPushButton("Iniciar carga de documentos")
        load_button.setFixedSize(220, 40)
        load_button.setStyleSheet(self.init_charge_button_style())
        load_button.setCursor(Qt.PointingHandCursor)
        load_button.clicked.connect(self.handle_path_input)

        path_layout.addWidget(self.path_input)
        path_layout.addWidget(path_button)
        path_layout.addWidget(load_button)

        padded_layout.addLayout(path_layout)
        
        content_layout.addWidget(padded_container)


    def add_radio_option_list(self, content_layout):
        title = QLabel("Configuración de interacción con el sistema")
        title.setStyleSheet(self.title_style())
        content_layout.addWidget(title)
        
        model_info = QLabel("Seleccione cómo gestionar el contenido de los documentos. (Recuerde que cambiar este ajuste conllevará recalcular los embeddings.)")
        content_layout.addWidget(model_info)

        padded_container = QWidget()
        padded_layout = QVBoxLayout()
        padded_layout.setContentsMargins(10, 0, 10, 0)
        padded_container.setLayout(padded_layout)

        self.radio_text = QRadioButton("    Generar embeddings con el documento completo.")
        self.radio_llm = QRadioButton("    Utilizar LLM Llama3.2 para utilizar embeddings de un resumen del documento.")
        self.radio_entities = QRadioButton("    Extraer entidades más importantes del texto y utilizarlas para generar los embeddings.")

        for radio in [self.radio_text, self.radio_llm, self.radio_entities]:
            radio.setCursor(Qt.PointingHandCursor)
            radio.setStyleSheet(self.text_style())
            padded_layout.addWidget(radio)

        self.interaction_group = QButtonGroup()
        self.interaction_group.addButton(self.radio_text)
        self.interaction_group.addButton(self.radio_llm)
        self.interaction_group.addButton(self.radio_entities)

        self.radio_text.setChecked(self.old_config["all_doc"])
        self.radio_llm.setChecked(self.old_config["summarize"])
        self.radio_entities.setChecked(self.old_config["most_important_entities"])

        content_layout.addWidget(padded_container)

    def update_model_selection(self, selected_index):
        for i, button in enumerate(self.model_buttons):
            if i == selected_index:
                button.setText("Seleccionado")
                button.setStyleSheet(self.model_selected_style())
            else:
                button.setText("Seleccionar")
                button.setStyleSheet(self.model_not_selected_style())
        self.selected_model_index = selected_index
        self.selected_model = self.models_data[selected_index]

        
    def show_confirmation_dialog(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Confirmar guardado")
        dialog.setText("¿Deseas guardar la configuración actual?")
        
        btn_aceptar = dialog.addButton("Aceptar", QMessageBox.AcceptRole)
        dialog.addButton("Cancelar", QMessageBox.RejectRole)
        
        dialog.exec()

        if dialog.clickedButton() == btn_aceptar:
            self.save_configuration()
    
    def save_configuration(self):
        path = self.path_input.text()
        embedding_model = self.selected_model["name"]
        
        content_management = {
            "all_doc": self.radio_text.isChecked(),
            "summarize": self.radio_llm.isChecked(),
            "most_important_entities": self.radio_entities.isChecked()
        }

        recharge = self.controller.update_config_document(path, content_management, embedding_model)
        if recharge:
            self.progress_dialog = QProgressDialog("Indexando archivos...", "Cancelar", 0, 0, self)
            self.progress_dialog.setWindowTitle("Indexando")
            self.progress_dialog.setWindowModality(Qt.ApplicationModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setValue(0)
            self.progress_dialog.show()
            
            self.controller.thread_function(self.update_progress, self.progress_dialog)

    def add_models(self, content_layout):
        title = QLabel("Selección de modelos de embeddings")
        title.setStyleSheet(self.title_style())
        content_layout.addWidget(title)

        padded_container = QWidget()
        padded_layout = QVBoxLayout()
        padded_layout.setContentsMargins(10, 0, 10, 0)
        padded_container.setLayout(padded_layout)

        model_info = QLabel("Elige el modelo de embedding a utilizar para gestionar la información de los documentos. (Recuerde que cambiar el modelo conlleva recalcular los embeddings.)")
        model_info.setStyleSheet(self.text_style())
        model_info.setWordWrap(True)
        padded_layout.addWidget(model_info)

        models_container = QWidget()
        models_layout = QHBoxLayout()
        models_layout.setContentsMargins(0, 0, 0, 0)
        models_layout.setSpacing(20)
        models_container.setLayout(models_layout)
        padded_layout.addWidget(models_container)

        self.model_buttons = []
        self.selected_model_index = None
        self.models_data = self.controller.load_embedding_models_file()

        for idx, model in enumerate(self.models_data):
            model_card = QFrame()
            model_card.setFrameShape(QFrame.StyledPanel)
            model_card.setStyleSheet(self.frame_style())

            model_layout = QVBoxLayout(model_card)
            model_layout.setContentsMargins(20, 20, 20, 20)
            model_layout.setSpacing(10)

            model_name = QLabel(f"Modelo: {model.get('name', 'Desconocido')}")
            model_name.setStyleSheet("font-size: 16px; font-weight: bold;")
            model_layout.addWidget(model_name)

            specs_text = (
                f"• Tamaño: {model.get('size', 'N/A')}\n"
                f"• Contexto: {model.get('context', 'N/A')}\n"
                f"• Lenguaje: {model.get('language', 'N/A')}"
            )

            specs = QLabel(specs_text)
            specs.setStyleSheet("font-size: 14px;")
            specs.setWordWrap(True)
            model_layout.addWidget(specs)

            if self.old_config["embedding_model"] == model["name"]:
                select_text = "Seleccionado"
                select_style = self.model_selected_style()
                self.selected_model = model
                self.selected_model_index = idx
            else:
                select_text = "Seleccionar"
                select_style = self.model_not_selected_style()
            select_button = QPushButton(select_text)
            select_button.setCursor(Qt.PointingHandCursor)
            select_button.setStyleSheet(select_style)

            def make_on_click(i):
                def on_click():
                    self.update_model_selection(i)
                return on_click

            select_button.clicked.connect(make_on_click(idx))
            self.model_buttons.append(select_button)
            model_layout.addWidget(select_button)

            models_layout.addWidget(model_card)

        content_layout.addWidget(padded_container)
    
    def create_content_area(self):
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignTop) 

        self.add_path_input(content_layout)
        self.add_radio_option_list(content_layout)
        self.add_models(content_layout)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        
        save_button = QPushButton("Guardar configuración")
        save_button.setFixedSize(220, 40)
        save_button.setStyleSheet(self.init_charge_button_style())
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self.show_confirmation_dialog)

        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(save_button)
        button_container.setLayout(button_layout)

        content_layout.addWidget(button_container)

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
        
    def title_style(self):
        return """
            QLabel {
                font-size: 16px; 
                font-weight: bold; 
                color: #7bab8c;
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
    def frame_style(self):
        return """
            QFrame {
                background-color: #f7f7f7;
                border-radius: 10px;
            }
            """
    
    def model_select_style(self):
        return """
            QPushButton {
                color: #0066cc;
                background: transparent;
                border: none;
                font-size: 14px;
                text-decoration: underline;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #7bab8c;
            }
        """
        
    def model_selected_style(self):
        return """
            QPushButton {
                color: #7bab8c;
                background: transparent;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
        """
        
    def model_not_selected_style(self):
        return"""
            QPushButton {
                color: #0066cc;
                background: transparent;
                border: none;
                font-size: 14px;
                text-decoration: underline;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #7bab8c;
            }
        """