"""
Improved File Selection UI with Batch Size

This module provides a UI for selecting input files/directories with improved feedback
and specifying batch size.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QSpinBox,
    QRadioButton, QButtonGroup, QGroupBox, QFormLayout,
    QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from src.utils.constants import UI


class FileSelectionUI(QMainWindow):
    """Improved UI for file/directory selection and batch size input."""
    
    def __init__(self):
        super().__init__()
        # Set window properties
        self.setWindowTitle(UI["WINDOW_TITLE"])
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        # Add title
        title_label = QLabel(UI["TITLE"])
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        # Add description
        description_label = QLabel(UI["DESCRIPTION"])
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description_label)
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        # Create selection mode group with visual indicators
        selection_group = QGroupBox(UI["SELECTION_GROUP"])
        selection_layout = QHBoxLayout(selection_group)
        # File selection option
        file_option = QWidget()
        file_layout = QVBoxLayout(file_option)
        file_icon_label = QLabel(UI["FILE_ICON"])
        file_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_icon_label.setStyleSheet("font-size: 36px;")
        self.file_radio = QRadioButton(UI["FILE_RADIO"])
        self.file_radio.setChecked(True)  # Default to file selection
        file_layout.addWidget(file_icon_label)
        file_layout.addWidget(self.file_radio, alignment=Qt.AlignmentFlag.AlignCenter)
        # Directory selection option
        dir_option = QWidget()
        dir_layout = QVBoxLayout(dir_option)
        dir_icon_label = QLabel(UI["DIR_ICON"])
        dir_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dir_icon_label.setStyleSheet("font-size: 36px;")
        self.directory_radio = QRadioButton(UI["DIR_RADIO"])
        dir_layout.addWidget(dir_icon_label)
        dir_layout.addWidget(self.directory_radio, alignment=Qt.AlignmentFlag.AlignCenter)
        # Add options to selection layout
        selection_layout.addWidget(file_option)
        selection_layout.addWidget(dir_option)
        # Group radio buttons
        self.selection_group = QButtonGroup()
        self.selection_group.addButton(self.file_radio, 1)
        self.selection_group.addButton(self.directory_radio, 2)
        self.selection_group.buttonClicked.connect(self.update_ui_for_selection_type)
        # Add selection group to main layout
        main_layout.addWidget(selection_group)
        # Create file selection area
        self.file_selection_group = QGroupBox(UI["FILE_SELECTION_GROUP"])
        file_selection_layout = QVBoxLayout(self.file_selection_group)
        # Add file path display
        self.file_path_display = QLineEdit()
        self.file_path_display.setPlaceholderText(UI["FILE_PATH_PLACEHOLDER"])
        self.file_path_display.setReadOnly(True)
        # Add browse button
        self.browse_file_button = QPushButton(UI["BROWSE_FILE_BUTTON"])
        self.browse_file_button.clicked.connect(self.browse_for_file)
        file_selection_layout.addWidget(self.file_path_display)
        file_selection_layout.addWidget(self.browse_file_button)
        # Create directory selection area
        self.dir_selection_group = QGroupBox(UI["DIR_SELECTION_GROUP"])
        dir_selection_layout = QVBoxLayout(self.dir_selection_group)
        # Add directory path display
        self.dir_path_display = QLineEdit()
        self.dir_path_display.setPlaceholderText(UI["DIR_PATH_PLACEHOLDER"])
        self.dir_path_display.setReadOnly(True)
        # Add browse button
        self.browse_dir_button = QPushButton(UI["BROWSE_DIR_BUTTON"])
        self.browse_dir_button.clicked.connect(self.browse_for_directory)
        dir_selection_layout.addWidget(self.dir_path_display)
        dir_selection_layout.addWidget(self.browse_dir_button)
        # Add selection areas to main layout (only one will be visible at a time)
        main_layout.addWidget(self.file_selection_group)
        main_layout.addWidget(self.dir_selection_group)
        # Initially hide directory selection
        self.dir_selection_group.setVisible(False)
        # Create batch size input area
        batch_group = QGroupBox(UI["BATCH_GROUP"])
        batch_layout = QFormLayout(batch_group)
        self.batch_size_input = QSpinBox()
        self.batch_size_input.setMinimum(1)
        self.batch_size_input.setMaximum(100)
        self.batch_size_input.setValue(5)  # Default batch size is 5
        self.batch_size_input.setToolTip(UI["BATCH_SIZE_TOOLTIP"])
        batch_layout.addRow(UI["BATCH_SIZE_LABEL"], self.batch_size_input)
        main_layout.addWidget(batch_group)
        # Add stretch to push buttons to bottom
        main_layout.addStretch(1)
        # Create buttons area
        buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton(UI["CANCEL_BUTTON"])
        self.cancel_button.clicked.connect(self.close)
        self.process_button = QPushButton(UI["PROCESS_BUTTON"])
        self.process_button.clicked.connect(self.process_clicked)
        self.process_button.setEnabled(False)  # Disabled until path is selected
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.process_button)
        main_layout.addLayout(buttons_layout)
    
    def update_ui_for_selection_type(self):
        """Update UI based on whether file or directory is selected."""
        if self.file_radio.isChecked():
            self.file_selection_group.setVisible(True)
            self.dir_selection_group.setVisible(False)
            # Update process button based on file selection
            self.process_button.setEnabled(bool(self.file_path_display.text()))
        else:
            self.file_selection_group.setVisible(False)
            self.dir_selection_group.setVisible(True)
            # Update process button based on directory selection
            self.process_button.setEnabled(bool(self.dir_path_display.text()))
    
    def browse_for_file(self):
        """Open file dialog and update UI with selected file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            UI["FILE_SELECTION_GROUP"],
            "",  # Start directory
            "All Files (*)"
        )
        if file_path:
            self.file_path_display.setText(file_path)
            self.process_button.setEnabled(True)
            # Update window title with selected file
            filename = os.path.basename(file_path)
            self.setWindowTitle(f"{UI['WINDOW_TITLE']} - {filename}")
    
    def browse_for_directory(self):
        """Open directory dialog and update UI with selected directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            UI["DIR_SELECTION_GROUP"],
            "",  # Start directory
            QFileDialog.Option.ShowDirsOnly
        )
        if directory:
            self.dir_path_display.setText(directory)
            self.process_button.setEnabled(True)
            # Update window title with selected directory
            dirname = os.path.basename(directory)
            self.setWindowTitle(f"{UI['WINDOW_TITLE']} - {dirname}/")
    
    def get_selected_path(self):
        """Get the currently selected path (file or directory)."""
        if self.file_radio.isChecked():
            return self.file_path_display.text()
        else:
            return self.dir_path_display.text()
    
    def process_clicked(self):
        """Handle process button click."""
        path = self.get_selected_path()
        batch_size = self.batch_size_input.value()
        # Additional validation (should not be needed due to UI constraints)
        if not path or not os.path.exists(path):
            QMessageBox.critical(
                self,
                UI["PATH_ERROR_TITLE"],
                UI["PATH_ERROR_MSG"]
            )
            return
        # Show confirmation with selected options
        input_type = "file" if self.file_radio.isChecked() else "directory"
        QMessageBox.information(
            self,
            UI["PROCESSING_STARTED_TITLE"],
            f"{UI['PROCESSING_STARTED_MSG']}\nInput {input_type}: {path}\nBatch Size: {batch_size}"
        )
        # Here you would call your processing function
        # For example: process_files(path, batch_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set application style
    app.setStyle("Fusion")
    # Create and show the window
    window = FileSelectionUI()
    window.show()
    # Run the application event loop
    sys.exit(app.exec())