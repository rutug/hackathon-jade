import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QCheckBox, QRadioButton, QComboBox, 
    QSlider, QDial, QSpinBox, QDoubleSpinBox, QProgressBar, 
    QLCDNumber, QDateEdit, QTimeEdit, QDateTimeEdit, QFontComboBox,
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, 
    QTabWidget, QToolBar, QAction, QStatusBar, QMenuBar, QListWidget,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QGroupBox, QScrollArea, QSplitter
)
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap

class ComprehensivePyQtExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comprehensive PyQt5 Example - All Major Widgets")
        self.setGeometry(100, 100, 1000, 700)
        self.initUI()

    def initUI(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.createMenuBar()
        
        # Create toolbar
        self.createToolBar()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Create tab widget for organizing different widget categories
        tabs = QTabWidget()
        
        # Tab 1: Basic Input Widgets
        tab1 = self.createBasicInputTab()
        tabs.addTab(tab1, "Basic Input")
        
        # Tab 2: Selection Widgets
        tab2 = self.createSelectionTab()
        tabs.addTab(tab2, "Selection")
        
        # Tab 3: Display Widgets
        tab3 = self.createDisplayTab()
        tabs.addTab(tab3, "Display")
        
        # Tab 4: Date & Time Widgets
        tab4 = self.createDateTimeTab()
        tabs.addTab(tab4, "Date & Time")
        
        # Tab 5: Container Widgets
        tab5 = self.createContainerTab()
        tabs.addTab(tab5, "Containers")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)

    def createMenuBar(self):
        """Create menu bar with File and Edit menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        edit_menu.addAction(paste_action)

    def createToolBar(self):
        """Create toolbar with common actions"""
        toolbar = self.addToolBar('Main')
        
        new_action = QAction('New', self)
        toolbar.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openFile)
        toolbar.addAction(open_action)
        
        toolbar.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)

    def createBasicInputTab(self):
        """Create tab with basic input widgets"""
        tab = QWidget()
        layout = QGridLayout()
        
        # QLabel
        layout.addWidget(QLabel("QLabel:"), 0, 0)
        layout.addWidget(QLabel("This is a label"), 0, 1)
        
        # QLineEdit
        layout.addWidget(QLabel("QLineEdit:"), 1, 0)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter text here...")
        layout.addWidget(self.line_edit, 1, 1)
        
        # QTextEdit
        layout.addWidget(QLabel("QTextEdit:"), 2, 0)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter multiline text here...")
        layout.addWidget(self.text_edit, 2, 1)
        
        # QPushButton
        layout.addWidget(QLabel("QPushButton:"), 3, 0)
        button = QPushButton("Click Me!")
        button.clicked.connect(self.onButtonClick)
        layout.addWidget(button, 3, 1)
        
        # QFontComboBox
        layout.addWidget(QLabel("QFontComboBox:"), 4, 0)
        self.font_combo = QFontComboBox()
        layout.addWidget(self.font_combo, 4, 1)
        
        tab.setLayout(layout)
        return tab

    def createSelectionTab(self):
        """Create tab with selection widgets"""
        tab = QWidget()
        layout = QGridLayout()
        
        # QCheckBox
        layout.addWidget(QLabel("QCheckBox:"), 0, 0)
        checkbox_layout = QVBoxLayout()
        self.checkbox1 = QCheckBox("Option 1")
        self.checkbox2 = QCheckBox("Option 2")
        self.checkbox3 = QCheckBox("Option 3")
        checkbox_layout.addWidget(self.checkbox1)
        checkbox_layout.addWidget(self.checkbox2)
        checkbox_layout.addWidget(self.checkbox3)
        checkbox_widget = QWidget()
        checkbox_widget.setLayout(checkbox_layout)
        layout.addWidget(checkbox_widget, 0, 1)
        
        # QRadioButton
        layout.addWidget(QLabel("QRadioButton:"), 1, 0)
        radio_layout = QVBoxLayout()
        self.radio1 = QRadioButton("Choice A")
        self.radio2 = QRadioButton("Choice B")
        self.radio3 = QRadioButton("Choice C")
        self.radio1.setChecked(True)  # Set default selection
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        radio_widget = QWidget()
        radio_widget.setLayout(radio_layout)
        layout.addWidget(radio_widget, 1, 1)
        
        # QComboBox
        layout.addWidget(QLabel("QComboBox:"), 2, 0)
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Item 1", "Item 2", "Item 3", "Item 4"])
        layout.addWidget(self.combo_box, 2, 1)
        
        # QSlider
        layout.addWidget(QLabel("QSlider:"), 3, 0)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.onSliderChange)
        layout.addWidget(self.slider, 3, 1)
        
        # QDial
        layout.addWidget(QLabel("QDial:"), 4, 0)
        self.dial = QDial()
        self.dial.setRange(0, 100)
        self.dial.setValue(25)
        layout.addWidget(self.dial, 4, 1)
        
        # QSpinBox
        layout.addWidget(QLabel("QSpinBox:"), 5, 0)
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 1000)
        self.spin_box.setValue(50)
        layout.addWidget(self.spin_box, 5, 1)
        
        # QDoubleSpinBox
        layout.addWidget(QLabel("QDoubleSpinBox:"), 6, 0)
        self.double_spin_box = QDoubleSpinBox()
        self.double_spin_box.setRange(0.0, 100.0)
        self.double_spin_box.setValue(25.5)
        self.double_spin_box.setDecimals(2)
        layout.addWidget(self.double_spin_box, 6, 1)
        
        tab.setLayout(layout)
        return tab

    def createDisplayTab(self):
        """Create tab with display widgets"""
        tab = QWidget()
        layout = QGridLayout()
        
        # QProgressBar
        layout.addWidget(QLabel("QProgressBar:"), 0, 0)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(75)
        layout.addWidget(self.progress_bar, 0, 1)
        
        # QLCDNumber
        layout.addWidget(QLabel("QLCDNumber:"), 1, 0)
        self.lcd_number = QLCDNumber()
        self.lcd_number.display(12345)
        layout.addWidget(self.lcd_number, 1, 1)
        
        # QListWidget
        layout.addWidget(QLabel("QListWidget:"), 2, 0)
        self.list_widget = QListWidget()
        self.list_widget.addItems(["List Item 1", "List Item 2", "List Item 3", "List Item 4"])
        layout.addWidget(self.list_widget, 2, 1)
        
        # QTableWidget
        layout.addWidget(QLabel("QTableWidget:"), 3, 0)
        self.table_widget = QTableWidget(3, 3)
        self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(f"Cell {row},{col}")
                self.table_widget.setItem(row, col, item)
        layout.addWidget(self.table_widget, 3, 1)
        
        tab.setLayout(layout)
        return tab

    def createDateTimeTab(self):
        """Create tab with date and time widgets"""
        tab = QWidget()
        layout = QGridLayout()
        
        # QDateEdit
        layout.addWidget(QLabel("QDateEdit:"), 0, 0)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit, 0, 1)
        
        # QTimeEdit
        layout.addWidget(QLabel("QTimeEdit:"), 1, 0)
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        layout.addWidget(self.time_edit, 1, 1)
        
        # QDateTimeEdit
        layout.addWidget(QLabel("QDateTimeEdit:"), 2, 0)
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.datetime_edit, 2, 1)
        
        tab.setLayout(layout)
        return tab

    def createContainerTab(self):
        """Create tab with container widgets"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # QGroupBox
        group_box = QGroupBox("QGroupBox Example")
        group_layout = QVBoxLayout()
        group_layout.addWidget(QCheckBox("Group Option 1"))
        group_layout.addWidget(QCheckBox("Group Option 2"))
        group_layout.addWidget(QPushButton("Group Button"))
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # QTreeWidget
        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabel("QTreeWidget")
        root = QTreeWidgetItem(tree_widget)
        root.setText(0, "Root Item")
        child1 = QTreeWidgetItem(root)
        child1.setText(0, "Child 1")
        child2 = QTreeWidgetItem(root)
        child2.setText(0, "Child 2")
        subchild = QTreeWidgetItem(child1)
        subchild.setText(0, "Subchild")
        tree_widget.expandAll()
        layout.addWidget(tree_widget)
        
        # QSplitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(QTextEdit("Left pane"))
        splitter.addWidget(QTextEdit("Right pane"))
        layout.addWidget(splitter)
        
        tab.setLayout(layout)
        return tab

    # Event handlers and utility methods
    def onButtonClick(self):
        """Handle button click event"""
        text = self.line_edit.text()
        if text:
            QMessageBox.information(self, "Button Clicked", f"You entered: {text}")
            self.statusBar().showMessage(f"Button clicked with text: {text}")
        else:
            QMessageBox.warning(self, "Warning", "Please enter some text first!")

    def onSliderChange(self, value):
        """Handle slider value change"""
        self.progress_bar.setValue(value)
        self.lcd_number.display(value)
        self.statusBar().showMessage(f"Slider value: {value}")

    def openFile(self):
        """Open file dialog"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            self.statusBar().showMessage(f"Selected file: {file_name}")

    def saveFile(self):
        """Save file dialog"""
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if file_name:
            self.statusBar().showMessage(f"File saved as: {file_name}")

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("PyQt5 Comprehensive Example")
    app.setApplicationVersion("1.0")
    
    # Create and show the main window
    window = ComprehensivePyQtExample()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
