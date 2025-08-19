from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QCheckBox, 
    QMessageBox, QProgressDialog, QSlider, QDoubleSpinBox, QSpacerItem, QSizePolicy
)

from PySide6.QtCore import Signal
from PySide6.QtCore import Qt, QSize, QThread, QObject
from PySide6.QtGui import QIcon

class FileIndexWorker(QObject):
    progress = Signal(int, int)
    finished = Signal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        self.controller.index_documents(progress_callback=self.progress.emit)
        self.finished.emit()

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
            
    def handle_path_input(self):
        path = self.path_input.text()
        if path != self.old_config["path"]:
            self.controller.update_path(path)
            self.old_config = self.controller.load_config_file()
            self.start_indexing()

    def update_progress(self, current, total):
        if self.progress_dialog:
            self.progress_dialog.setMaximum(total)
            self.progress_dialog.setValue(current)
            self.progress_dialog.setLabelText(f"Indexando archivos...\nDocumentos procesados: {current} / {total}")
            
    def add_path_input(self, content_layout):
        title = QLabel("Configuración de ruta de documentos")
        title.setStyleSheet(self.title_style())
        
        padded_container = QWidget()
        padded_layout = QVBoxLayout()
        padded_layout.setContentsMargins(10, 10, 10, 10)
        padded_container.setLayout(padded_layout)
        padded_layout.addWidget(title)

        path_info = QLabel("Especifica la carpeta donde se encuentran los documentos que deseas consultar.")
        path_info.setStyleSheet(self.info_style())
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


    def add_search_options(self, content_layout):
        padded_container = QWidget()
        padded_layout = QVBoxLayout()
        padded_layout.setContentsMargins(10, 10, 10, 10)
        padded_container.setLayout(padded_layout)

        title_rag = QLabel("Configuración de interacción con el sistema (RAG)")
        title_rag.setStyleSheet(self.title_style())
        padded_layout.addWidget(title_rag)

        info_rag = QLabel(
            "Utilizar RAG (Retrieval-Augmented Generation) permite al modelo acceder a documentos relevantes "
            "durante la generación de respuestas. Si se desactiva, el modelo generará respuestas con los nombres "
            "de los documentos."
        )
        info_rag.setStyleSheet(self.info_style())
        info_rag.setWordWrap(True)
        padded_layout.addWidget(info_rag)

        self.checkbox_rag = QCheckBox("Usar RAG para generar la respuesta.")
        self.checkbox_rag.setCursor(Qt.PointingHandCursor)
        self.checkbox_rag.setStyleSheet(self.text_style())
        self.checkbox_rag.setChecked(self.old_config["checkbox_rag_value"])
        padded_layout.addWidget(self.checkbox_rag)

        padded_layout.addSpacing(20)

        title_similarity = QLabel("Configuración de interacción con el sistema (Similitud)")
        title_similarity.setStyleSheet(self.title_style())
        padded_layout.addWidget(title_similarity)

        info_threshold = QLabel(
            "Nivel de similitud mínimo (0.0 a 1.0). Este umbral determina qué tan similares deben ser los documentos "
            "para ser considerados relevantes. Un valor más alto significa que solo se considerarán documentos muy "
            "similares. Un valor más bajo permitirá que se muestren documentos menos similares. El valor por defecto "
            "es 0.7, lo que significa que se considerarán documentos con un 70% de similitud o más."
        )
        info_threshold.setStyleSheet(self.info_style())
        info_threshold.setWordWrap(True)
        padded_layout.addWidget(info_threshold)

        threshold_container = QWidget()
        threshold_layout = QHBoxLayout()
        threshold_layout.setContentsMargins(0, 0, 0, 0)
        threshold_container.setLayout(threshold_layout)

        self.slider_threshold = QSlider(Qt.Horizontal)
        self.slider_threshold.setRange(0, 100)
        self.slider_threshold.setValue(int(self.old_config.get("similarity_threshold", self.old_config["similarity_threshold_value"]) * 100))

        self.spinbox_threshold = QDoubleSpinBox()
        self.spinbox_threshold.setRange(0.0, 1.0)
        self.spinbox_threshold.setSingleStep(0.01)
        self.spinbox_threshold.setValue(self.old_config.get("similarity_threshold", self.old_config["similarity_threshold_value"]))

        self.slider_threshold.valueChanged.connect(
            lambda val: self.spinbox_threshold.setValue(val / 100.0)
        )
        self.spinbox_threshold.valueChanged.connect(
            lambda val: self.slider_threshold.setValue(int(val * 100))
        )

        threshold_layout.addWidget(self.slider_threshold)
        threshold_layout.addWidget(self.spinbox_threshold)
        padded_layout.addWidget(threshold_container)

        padded_layout.addSpacing(10)

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
            
    def start_indexing(self):
        self.progress_dialog = QProgressDialog("Indexando archivos...", "Cancelar", 0, 0, self)
        self.progress_dialog.setWindowTitle("Indexando")
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()

        self.thread = QThread()
        self.worker = FileIndexWorker(self.controller)
        self.worker.moveToThread(self.thread)

        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.progress_dialog.close)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def save_configuration(self):
        path = self.path_input.text()
        checkbox_rag_value = self.checkbox_rag.isChecked()
        similarity_threshold_value = self.spinbox_threshold.value()

        recharge = self.controller.update_config_document(path, checkbox_rag_value, similarity_threshold_value)
        if recharge:
            self.start_indexing()
          
    def create_content_area(self):
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignTop)

        self.add_path_input(content_layout)
        self.add_search_options(content_layout)

        content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        save_button = QPushButton("Guardar configuración")
        save_button.setFixedSize(220, 40)
        save_button.setStyleSheet(self.init_charge_button_style())
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self.show_confirmation_dialog)

        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setContentsMargins(0, 0, 0, 20)
        button_layout.addWidget(save_button)
        button_container.setLayout(button_layout)

        content_layout.addWidget(button_container)

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
        
    def title_style(self):
        return """
            QLabel {
                font-size: 16px; 
                font-weight: bold; 
                color: #7bab8c;
            }
        """
        
    def info_style(self):
        return """
            QLabel {
                font-size: 14px; 
                color: #666;
                margin-bottom: 10px;
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