from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit, 
    QStyle
)
from PyQt6.QtCore import Qt
from cua_signals import CuaSignal
from database.database_service import DatabaseService
from datetime import datetime, date
from history_table import HistoryTable


class MainWindow(QMainWindow):
    """
        The main user interface for the Core Utility App. 
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Core Utility App")
        self.setGeometry(100,100, 400, 600)

        #Establish database connectivity
        self.db = DatabaseService()
        self.db.add_table(["users", "history"])

        self.history_table = HistoryTable()

        self.signals = CuaSignal()
        self.counter_value = 0

        widget = QWidget()

       
        username_layout = QHBoxLayout()
        self.username_input = QLineEdit()

        self.username_placeholder = "Enter user name"
        self.username_input.setPlaceholderText(self.username_placeholder)
        save_btn = QPushButton("Save")
        
        username_layout.addWidget(self.username_input)
        username_layout.addWidget(save_btn)


        self.username_input.setStyleSheet(
            "background: white; border-width: 1vw; border-radius: 1px; color: black"
        )
        QPushButton.setStyleSheet(save_btn,
            "background: green; color: black"
        )
       


        save_btn.pressed.connect(self.get_user_data)

        main_layout = QVBoxLayout(widget)

        counter_layout = QHBoxLayout()

        increment_btn = QPushButton("-->")
        decrement_btn = QPushButton("<--")
        self.counter_label = QLabel(str(self.counter_value))

        QPushButton.setStyleSheet(increment_btn,
            "background: green; color: black"
        )
        QPushButton.setStyleSheet(decrement_btn,
            "background: green; color: black"
        )
        QLabel.setStyleSheet(self.counter_label,
            "background: white; border-width: 2vw; border-radius: 1px; color: black"
        )

        increment_btn.pressed.connect(self.counter_increment)
        decrement_btn.pressed.connect(self.counter_decrement)

        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        counter_layout.addWidget(decrement_btn)
        counter_layout.addWidget(self.counter_label)
        counter_layout.addWidget(increment_btn)

        main_layout.addWidget(self.history_table)
        main_layout.addLayout(username_layout)
        main_layout.addLayout(counter_layout)

        

        self.signals.increment.connect(self.update_counter)
        self.signals.decrement.connect(self.update_counter)
        self.signals.save_data.connect(self.save_user_data)

        self.setCentralWidget(widget)

    def get_user_data(self):
        username = self.username_input.text().strip() #Removes all the trailling spaces from the username
        counter_value = self.counter_value
        now = datetime.now()
        created_at = date(now.year, now.month, now.day)

        if not username:
            print("Enter the username before trying to save")
        else:
            self.signals.save_data.emit((username, counter_value, created_at))
        # Resetting the user input
        self.username_input.setText("") 
        

    def save_user_data(self, data: tuple):
        user_data = self.db.read_a_user(username=data[0])
        history = None


        if not user_data:
            try:
                self.db.create_user(data[0], data[2])
            except Exception as e:
                print(f"Unable to save user information to the database.\n{e}")
            try:
                self.db.create_history(username=data[0] ,history_name="counter", history_value=data[1], updated_at=data[2])
            except Exception as e:
                print(f"Unable to save user history.\nError: {e}")
        #If the user exists, add the history in the history table
        else:
            #created_at field must be updated with thecurrent date
            now = datetime.now()
            updated_at = str(date(now.year, now.month, now.day))
            response = self.db.create_history(username=data[0], history_name="counter", history_value=data[1], updated_at=updated_at)

            if not response:
                print("Unable to add new user history")
            else:
                print("New user hisory added")
        
        #Populate the history table
        if user_data:
            try:
                history = self.db.read_all_history(username=data[0])
                if history:
                    self.history_table.clear_history()
                    print(f"Restoring {data[0]} histories")
                    self.history_table.restore_history(histories=history)
            except Exception as e:
                print(f"Unable to restore history for {data[0]}.\nError: {e}")
                    
        

    
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

