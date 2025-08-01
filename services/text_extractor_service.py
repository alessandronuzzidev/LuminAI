from services.embeddings_service import EmbeddingsService
from services.docx_loader import DOCXLoader
from services.json_loader import JSONLoader
from services.markdown_loader import MarkdownLoader
from services.pdf_loader import PDFLoader
from services.pptx_loader import PPTXLoader
from services.txt_loader import TXTLoader
from services.xlsx_loader import XLSXLoader
from services.yaml_loader import YAMLLoader

import os
from pathlib import Path

class TextExtractorService:
    
    def __init__(self):
        self.loaders = {
            ".docx": DOCXLoader(),
            ".json": JSONLoader(),
            ".md": MarkdownLoader(),
            ".pdf": PDFLoader(),
            ".pptx": PPTXLoader(),
            ".txt": TXTLoader(),
            ".xlsx": XLSXLoader(),
            ".yaml": YAMLLoader()
        }
    
    def extract_text(self, path_str):
        folder = os.path.dirname(path_str)  # "/ruta/a/carpeta"
        file = os.path.basename(path_str)
        
        embedding_service = EmbeddingsService()
        path = Path(path_str)
        suffix = path.suffix
        doc = self.loaders[suffix].load(folder, file)
        metadata = {}
        
        for k, v in doc.items():
            if k != "content":
                metadata[k] = v
                
        metadata["path"] = path_str
        print(path_str)
        print(doc["content"])
        print(metadata)
        
        embedding_service.save_documents(doc["content"], metadata)