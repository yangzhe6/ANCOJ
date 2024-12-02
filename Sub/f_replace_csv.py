import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class CsvHeaderEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Header Editor")
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()
        self.setGeometry(10, 50, int(screen_width * 0.15), int(screen_height * 0.8))
        self.csv_files = []
        self.file_names = []
        self.current_index = -1
        self.current_data = None
        self.backup_data = None
        self.main_layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        file_layout = QVBoxLayout()
        self.file_label = QLabel("", self)
        self.file_label.setStyleSheet("font-weight: bold; color: darkred; font-size: 40px; margin: 0px;")
        self.file_label.setAlignment(Qt.AlignLeft)
        file_layout.addWidget(self.file_label)
        jump_layout = QHBoxLayout()
        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("输入文件名")
        self.index_input.setFont(QFont("Arial"))
        self.index_input.returnPressed.connect(self.jump_to_file)
        jump_layout.addWidget(QLabel("跳转:", self))
        jump_layout.addWidget(self.index_input)
        file_layout.addLayout(jump_layout)
        self.main_layout.addLayout(file_layout)
        self.header_table = QTableWidget()
        self.header_table.setStyleSheet(
            """
            QTableWidget { font-size: 25px; }
            QTableWidget::item { text-align: center; }
            """
        )
        self.header_table.horizontalHeader().setStretchLastSection(True)
        self.header_table.verticalHeader().setVisible(True)
        self.header_table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.header_table.cellChanged.connect(self.on_cell_changed)
        self.main_layout.addWidget(self.header_table)

        button_layout = QHBoxLayout()
        self.load_folder_btn = QPushButton("加载文件夹")
        self.load_folder_btn.clicked.connect(self.load_folder)
        button_layout.addWidget(self.load_folder_btn)

        self.prev_file_btn = QPushButton("上一文件")
        self.prev_file_btn.clicked.connect(lambda: self.navigate_file(-1))
        button_layout.addWidget(self.prev_file_btn)

        self.next_file_btn = QPushButton("下一文件")
        self.next_file_btn.clicked.connect(lambda: self.navigate_file(1))
        button_layout.addWidget(self.next_file_btn)

        self.undo_btn = QPushButton("撤销更改")
        self.undo_btn.clicked.connect(self.undo_changes)
        button_layout.addWidget(self.undo_btn)
        
        self.replace_btn = QPushButton("替换表头")
        self.replace_btn.clicked.connect(self.replace_header)
        
        button_layout.addWidget(self.replace_btn)
        self.main_layout.addLayout(button_layout)
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择CSV文件夹")
        if folder_path:
            self.csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".csv")]
            self.file_names = [os.path.splitext(os.path.basename(f))[0] for f in self.csv_files]
            self.current_index = -1
            self.navigate_file(1)

    def navigate_file(self, direction):
        if not self.csv_files:
            self.show_warning("警告", "请先加载一个文件夹！")
            return
        self.current_index += direction
        if 0 <= self.current_index < len(self.csv_files):
            file_path = self.csv_files[self.current_index]
            file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
            self.file_label.setText(f"{file_name_without_extension}")
            self.load_csv(file_path)
        else:
            self.current_index -= direction

    def jump_to_file(self):
        if not self.csv_files:
            self.show_warning("警告", "请先加载一个文件夹！")
            return
        input_name = self.index_input.text().strip()
        if input_name in self.file_names:
            self.current_index = self.file_names.index(input_name)
            self.navigate_file(0)
        else:
            self.show_warning("警告", "文件名不存在，请检查输入！")

    def load_csv(self, file_path):
        try:
            self.current_data = pd.read_csv(file_path)
            self.backup_data = self.current_data.copy()
            self.display_headers()
        except Exception as e:
            self.show_critical("错误", f"无法加载文件: {e}")

    def display_headers(self):
        if self.current_data is not None:
            headers = list(self.current_data.columns)
            self.header_table.setRowCount(len(headers))
            self.header_table.setColumnCount(1)
            self.header_table.setHorizontalHeaderLabels(["表头"])
            for row, header in enumerate(headers):
                item = QTableWidgetItem(header)
                item.setToolTip("原表头: " + header)
                item.setTextAlignment(Qt.AlignCenter)
                self.header_table.setItem(row, 0, item)
            if self.header_table.rowCount() > 0:
                self.header_table.setCurrentCell(0, 0)

    def replace_header(self):
        if self.current_data is not None:
            try:
                new_headers = [
                    self.header_table.item(row, 0).text() if self.header_table.item(row, 0) else ""
                    for row in range(self.header_table.rowCount())
                ]
                if any(not header.strip() for header in new_headers):
                    self.show_warning("警告", "新表头不能为空！")
                    return
                self.current_data.columns = new_headers
                file_path = self.csv_files[self.current_index]
                self.current_data.to_csv(file_path, index=False)
                self.show_information("成功", "表头已成功替换！")
                self.display_headers()
            except Exception as e:
                self.show_critical("错误", f"替换表头时出现问题: {e}")

    def undo_changes(self):
        if self.backup_data is not None:
            try:
                self.current_data = self.backup_data.copy()
                file_path = self.csv_files[self.current_index]
                self.current_data.to_csv(file_path, index=False)
                self.show_information("成功", "已撤销更改！")
                self.display_headers()
            except Exception as e:
                self.show_critical("错误", f"撤销更改时出现问题: {e}")

    def on_cell_changed(self, row, col):
        next_row = row + 1
        if next_row < self.header_table.rowCount():
            self.header_table.setCurrentCell(next_row, col)

    def show_information(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.show()
        QTimer.singleShot(300, msg_box.close)

    def show_warning(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.show()
        QTimer.singleShot(300, msg_box.close)

    def show_critical(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.show()
        QTimer.singleShot(300, msg_box.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = CsvHeaderEditor()
    editor.show()
    sys.exit(app.exec_())