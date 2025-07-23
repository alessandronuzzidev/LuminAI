from abstract_file_loader import AbstractFileLoader
import fitz

class PDFLoader(AbstractFileLoader):
    def load(self, file_path):
        """
        Load the content from the specified PDF file path.

        :param file_path: The path to the PDF file to be loaded.
        :return: The text content of the PDF file.
        """
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    def save(self, file_path, content):
        """
        Save the content to a new PDF file.

        :param file_path: The path where the PDF should be saved.
        :param content: The text content to be saved in the PDF.
        """
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), content)  # Insert text at (72, 72) position
        doc.save(file_path)
        doc.close()