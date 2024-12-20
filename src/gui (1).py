# src/gui.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QTreeWidget, 
    QTreeWidgetItem, QFrame
)
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter
from PyQt5.QtCore import Qt, QRect

from dns_resolver import DNSResolver

class StyledFrame(QFrame):
    """Custom styled frame with gradient background"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(78, 129, 190, 255), 
                    stop:1 rgba(117, 184, 255, 255));
                border-radius: 10px;
                color: white;
                padding: 10px;
            }
        """)

class DNSResolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.setWindowTitle("DNS Resolver Simulator")
        self.setGeometry(100, 100, 900, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f8;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                color: black;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
        """)
        
        # Central Widget Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Project Title
        project_title = QLabel("DNS Resolver Simulator")
        project_title.setFont(QFont('Arial', 20, QFont.Bold))
        project_title.setAlignment(Qt.AlignCenter)
        project_title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(project_title)
        
        # Project Attribution
        attribution = QLabel("Project by Sumaiya, Brooj, and Raiya")
        attribution.setFont(QFont('Arial', 12))
        attribution.setAlignment(Qt.AlignCenter)
        attribution.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        main_layout.addWidget(attribution)
        
        # Styled Input Frame
        input_frame = StyledFrame()
        input_layout = QHBoxLayout()
        input_frame.setLayout(input_layout)
        
        # Domain Input
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter domain (e.g., www.example.com)")
        self.domain_input.setStyleSheet("""
            QLineEdit {
            color:black;
                padding: 10px;
                font-size: 14px;
                border: none;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 5px;
            }
        """)
        
        # Resolve Button
        resolve_button = QPushButton("Resolve DNS")
        resolve_button.clicked.connect(self.resolve_domain)
        resolve_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        
        input_layout.addWidget(self.domain_input)
        input_layout.addWidget(resolve_button)
        main_layout.addWidget(input_frame)
        
        # Mapping Tree
        self.mapping_tree = QTreeWidget()
        self.mapping_tree.setStyleSheet("""
            QTreeWidget {
            color:white;
                background-color: black;
                border-radius: 10px;
                padding: 10px;
            }
            QTreeWidget::item {
                padding: 5px;
                margin: 2px;
                border-radius: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
                color: black;
            }
        """)
        self.mapping_tree.setHeaderLabels(["DNS Resolution Mapping"])
        main_layout.addWidget(self.mapping_tree)
        
        # Steps Display
        steps_label = QLabel("Resolution Steps:")
        steps_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        main_layout.addWidget(steps_label)
        
        self.steps_display = QTextEdit()
        self.steps_display.setReadOnly(True)
        self.steps_display.setStyleSheet("""
            QTextEdit {
                background-color: black;
                border-radius: 10px;
                padding: 10px;
                font-family: Consolas, monospace;
            }
        """)
        main_layout.addWidget(self.steps_display)

    def resolve_domain(self):
        domain = self.domain_input.text().strip()
        
        if not domain:
            QMessageBox.warning(self, "Input Error", "Please enter a domain name")
            return
        
        # Clear previous results
        self.mapping_tree.clear()
        self.steps_display.clear()
        
        try:
            result = DNSResolver.resolve_domain(domain)
            
            # Display Steps
            steps = "\n".join(result.get('resolution_steps', []))
            self.steps_display.setPlainText(steps)
            
            # Populate Mapping Tree
            mapping = result.get('resolution_mapping', {})
            self.populate_mapping_tree(mapping)
        
        except Exception as e:
            QMessageBox.critical(self, "Resolution Error", str(e))

    def populate_mapping_tree(self, mapping):
        """
        Populate the QTreeWidget with DNS resolution mapping
        """
        # Root item
        root = QTreeWidgetItem(self.mapping_tree, [f"DNS Resolution for {mapping.get('domain', 'Unknown')}"])
        root.setBackground(0, QColor(52, 152, 219, 50))  # Soft blue background
        
        # IP and Domain Details
        details = QTreeWidgetItem(root, ["Domain Details"])
        details.addChild(QTreeWidgetItem(["Domain: " + str(mapping.get('domain', 'N/A'))]))
        details.addChild(QTreeWidgetItem(["IP Address: " + str(mapping.get('ip_address', 'N/A'))]))
        details.setBackground(0, QColor(46, 204, 113, 50))  # Soft green background
        
        # Resolution Path
        path = QTreeWidgetItem(root, ["Resolution Path"])
        for step in mapping.get('resolution_path', []):
            step_item = QTreeWidgetItem([f"{step.get('stage', 'Unknown Stage')}"])
            step_item.addChild(QTreeWidgetItem(["Description: " + step.get('description', 'N/A')]))
            step_item.addChild(QTreeWidgetItem(["Status: " + step.get('status', 'N/A')]))
            
            # Add IP if available
            if 'ip_address' in step:
                step_item.addChild(QTreeWidgetItem(["IP: " + step.get('ip_address', 'N/A')]))
            
            path.addChild(step_item)
        path.setBackground(0, QColor(241, 196, 15, 50))  # Soft yellow background
        
        # Expand all items
        self.mapping_tree.expandAll()

# Run GUI directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DNSResolverApp()
    window.show()
    sys.exit(app.exec_())
