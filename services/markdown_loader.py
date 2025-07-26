from abstract_file_loader import AbstractFileLoader
import os


class MarkdownLoader(AbstractFileLoader):
    
    def __init__(self):
        super().__init__()
    
    def load(self, file_path, file_name):
        """
        Load the content from the specified Markdown file path.
        :param file_path: The path to the PDF file to be loaded.
        :param file_name: The name of the PDF file to be loaded.
        :return: A dictionary containing the file name, path, extension, content, and size in bytes.
        """
        full_path = os.path.join(file_path, file_name)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        doc = {
            "name": file_name,
            "path": full_path,
            "extension": "md",
            "content": content.strip().replace("\n", " "),
            "size_bytes": os.path.getsize(full_path)
        }
        return doc
    
    def exists(self, file_path, file_name):
        """
        Check if the specified PDF file exists.

        :param file_path: The path to the PDF file to check.
        :return: True if the file exists, False otherwise.
        """
        return os.path.exists(os.path.join(file_path, file_name)) and os.path.isfile(os.path.join(file_path, file_name))
