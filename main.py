import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def main() -> None:
    """
        The main function contructs the user interface using the system arguments
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()