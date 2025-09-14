import sys
from PyQt6.QtWidgets import QApplication
from src.gui.file_selection_ui import FileSelectionUI

def main():
    # Create the application first
    app = QApplication(sys.argv)
    
    # Then create and show the UI
    window = FileSelectionUI()
    window.show()
    
    # Run the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()