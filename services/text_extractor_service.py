import services.embeddings_lib as embedding
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
        if not os.path.isfile(path_str):
            return
        
        folder = os.path.dirname(path_str)
        file = os.path.basename(path_str)
        path = Path(path_str)
        suffix = path.suffix
        if suffix not in self.loaders.keys():
            return
        
        doc = self.loaders[suffix].load(folder, file)
        return doc
    
    def extract_and_save_text(self, path_str):
        if path_str.__contains__(".DS_Store"):
            return
        doc = self.extract_text(path_str)
        metadata = {}
        
        if doc.items():
            for k, v in doc.items():
                if k != "content":
                    metadata[k] = v
                    
            metadata["path"] = path_str

            if doc["content"] != "":
                embedding.save_documents(doc["content"], metadata)