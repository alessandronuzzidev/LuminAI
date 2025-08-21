from PySide6.QtWidgets import QApplication
import sys
from view.app_gui import App_GUI
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning
from services.control_monitor_lib import control_monitor

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass
    else:
        app = QApplication([])
        gui = App_GUI()
        gui.show()
    exit_code = app.exec()
    control_monitor("resume")
    sys.exit(exit_code)
    