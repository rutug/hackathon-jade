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


class ImprovedFileSelectionUI(QMainWindow):
    """Improved UI for file/directory selection and batch size input."""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("File Selection")
        self.setMinimumSize(600, 400)
        
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
        title_label = QLabel("Select Input Source")
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Add description
        description_label = QLabel("Choose a file or directory for processing")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # Create selection mode group with visual indicators
        selection_group = QGroupBox("Choose Input Type")
        selection_layout = QHBoxLayout(selection_group)
        
        # File selection option
        file_option = QWidget()
        file_layout = QVBoxLayout(file_option)
        
        file_icon_label = QLabel("📄")
        file_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_icon_label.setStyleSheet("font-size: 36px;")
        
        self.file_radio = QRadioButton("Single File")
        self.file_radio.setChecked(True)  # Default to file selection
        
        file_layout.addWidget(file_icon_label)
        file_layout.addWidget(self.file_radio, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Directory selection option
        dir_option = QWidget()
        dir_layout = QVBoxLayout(dir_option)
        
        dir_icon_label = QLabel("📁")
        dir_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dir_icon_label.setStyleSheet("font-size: 36px;")
        
        self.directory_radio = QRadioButton("Directory")
        
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
        self.file_selection_group = QGroupBox("Select File")
        file_selection_layout = QVBoxLayout(self.file_selection_group)
        
        # Add file path display
        self.file_path_display = QLineEdit()
        self.file_path_display.setPlaceholderText("No file selected")
        self.file_path_display.setReadOnly(True)
        
        # Add browse button
        self.browse_file_button = QPushButton("Browse for File...")
        self.browse_file_button.clicked.connect(self.browse_for_file)
        
        file_selection_layout.addWidget(self.file_path_display)
        file_selection_layout.addWidget(self.browse_file_button)
        
        # Create directory selection area
        self.dir_selection_group = QGroupBox("Select Directory")
        dir_selection_layout = QVBoxLayout(self.dir_selection_group)
        
        # Add directory path display
        self.dir_path_display = QLineEdit()
        self.dir_path_display.setPlaceholderText("No directory selected")
        self.dir_path_display.setReadOnly(True)
        
        # Add browse button
        self.browse_dir_button = QPushButton("Browse for Directory...")
        self.browse_dir_button.clicked.connect(self.browse_for_directory)
        
        dir_selection_layout.addWidget(self.dir_path_display)
        dir_selection_layout.addWidget(self.browse_dir_button)
        
        # Add selection areas to main layout (only one will be visible at a time)
        main_layout.addWidget(self.file_selection_group)
        main_layout.addWidget(self.dir_selection_group)
        
        # Initially hide directory selection
        self.dir_selection_group.setVisible(False)
        
        # Create batch size input area
        batch_group = QGroupBox("Processing Configuration")
        batch_layout = QFormLayout(batch_group)
        
        self.batch_size_input = QSpinBox()
        self.batch_size_input.setMinimum(1)
        self.batch_size_input.setMaximum(100)
        self.batch_size_input.setValue(5)  # Default batch size is 5
        self.batch_size_input.setToolTip("Number of items to process in each batch")
        
        batch_layout.addRow("Batch Size:", self.batch_size_input)
        
        main_layout.addWidget(batch_group)
        
        # Add stretch to push buttons to bottom
        main_layout.addStretch(1)
        
        # Create buttons area
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        self.process_button = QPushButton("Process")
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
            "Select File",
            "",  # Start directory
            "All Files (*)"
        )
        
        if file_path:
            self.file_path_display.setText(file_path)
            self.process_button.setEnabled(True)
            
            # Update window title with selected file
            filename = os.path.basename(file_path)
            self.setWindowTitle(f"File Selection - {filename}")
    
    def browse_for_directory(self):
        """Open directory dialog and update UI with selected directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            "",  # Start directory
            QFileDialog.Option.ShowDirsOnly
        )
        
        if directory:
            self.dir_path_display.setText(directory)
            self.process_button.setEnabled(True)
            
            # Update window title with selected directory
            dirname = os.path.basename(directory)
            self.setWindowTitle(f"File Selection - {dirname}/")
    
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
                "Path Error",
                "The selected path does not exist or is invalid."
            )
            return
        
        # Show confirmation with selected options
        input_type = "file" if self.file_radio.isChecked() else "directory"
        QMessageBox.information(
            self,
            "Processing Started",
            f"Starting processing with:\n"
            f"Input {input_type}: {path}\n"
            f"Batch Size: {batch_size}"
        )
        
        # Here you would call your processing function
        # For example: process_files(path, batch_size)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the window
    window = ImprovedFileSelectionUI()
    window.show()
    
    # Run the application event loop
    sys.exit(app.exec())