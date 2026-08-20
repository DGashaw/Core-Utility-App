from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import Qt
from cua_signals import CuaSignal


class MainWindow(QMainWindow):
    """
        The main user interface for the Core Utility App. 
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Core Utility App")
        self.setGeometry(100,100, 400, 600)

        self.signals = CuaSignal()
        self.counter_value = 0

        widget = QWidget()
        main_layout = QVBoxLayout(widget)

        counter_layout = QHBoxLayout()

        increment_btn = QPushButton("-->")
        decrement_btn = QPushButton("<--")
        self.counter_label = QLabel(str(self.counter_value))

        increment_btn.pressed.connect(self.counter_increment)
        decrement_btn.pressed.connect(self.counter_decrement)

        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        counter_layout.addWidget(decrement_btn)
        counter_layout.addWidget(self.counter_label)
        counter_layout.addWidget(increment_btn)

        main_layout.addLayout(counter_layout)
        self.signals.increment.connect(self.update_counter)
        self.signals.decrement.connect(self.update_counter)

        self.setCentralWidget(widget)
    def counter_increment(self):
        """
            Update the counter value when the increment button(-->) is pressed.
            Also emit the increment signal so that the counter user interface
            can be updated accordingly.
        """
        self.counter_value += 1
        self.signals.increment.emit(self.counter_value)

    def counter_decrement(self):
        """
            Update the counter value when the decrement button(<--) is pressed.
            Also emit the decrement signal so that the counter user interface
            can be updated accordingly.
            By default the counter value is set to be 0. This function ensures
            that by testing the current value of the counter.
        """
        if self.counter_value > 0:
            self.counter_value -= 1
        else:
            self.counter_value = 0
        self.signals.decrement.emit(self.counter_value)

    def update_counter(self, value):
        """
            Updates the counter which is defined as a label in the user-interface
        """
        self.counter_label.setText(str(value))
