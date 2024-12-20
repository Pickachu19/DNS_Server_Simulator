# src/main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui import DNSResolverApp

def main():
    """
    Main entry point for the DNS Resolver application
    """
    app = QApplication(sys.argv)
    dns_resolver_window = DNSResolverApp()
    dns_resolver_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
