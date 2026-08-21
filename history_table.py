from PyQt6.QtWidgets import(
    QTableWidget,
    QTableWidgetItem, 
    QVBoxLayout,
    QWidget

)



from database.database_service import DatabaseService

class HistoryTable(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["History Name", "History Value", "Created Date"])
        self.table.setStyleSheet(
            "QTableWidget { background-color: white; width: 100%}"
            "QTableWidget::item { alternate-background-color: white; color: black; border-bottom: 1px solid #ddd; }"
        )
        layout = QVBoxLayout()
        layout.addWidget(self.table)
       
        self.setStyleSheet("{ background-color: white; margin: 0px}")                         
        self.setLayout(layout)

    def restore_history(self, histories: list) -> None:
        if len(histories) > 0:
            for history in histories:
                self.add_table_item(history_name=history[0], history_value=history[1], created_at=history[2])

    def clear_history(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    def add_table_item(self, history_name: str, history_value: float, created_at: str):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(history_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(history_value)))
        self.table.setItem(row_position, 2, QTableWidgetItem(created_at))