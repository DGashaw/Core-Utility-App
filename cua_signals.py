from PyQt6.QtCore import pyqtSignal, QObject

class CuaSignal(QObject):
    """
        Defined signals for the Core Utility App
    """
    increment = pyqtSignal(int)
    decrement = pyqtSignal(int)
    save_data = pyqtSignal(tuple)
