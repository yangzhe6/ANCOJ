import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLineEdit, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt


class CsvHeaderEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Header Editor")
        self.setGeometry(100, 100, 1000, 700)

        # 初始化变量
        self.csv_files = []
        self.current_index = -1
        self.current_data = None
        self.backup_data = None

        # 主布局
        self.main_layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        # 文件展示
        file_layout = QHBoxLayout()
        self.file_label = QLabel("当前文件: 无")
        self.file_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333333;")
        file_layout.addWidget(self.file_label)

        # 跳转索引
        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("输入文件索引...")
        file_layout.addWidget(self.index_input)

        self.jump_button = QPushButton("跳转")
        self.jump_button.clicked.connect(self.jump_to_file)
        file_layout.addWidget(self.jump_button)

        self.main_layout.addLayout(file_layout)

        # 表头编辑区
        self.header_table = QTableWidget()
        self.header_table.setStyleSheet("QTableWidget { font-size: 14px; }")
        self.header_table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.header_table)

        # 按钮布局
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

        self.replace_btn = QPushButton("替换表头")
        self.replace_btn.clicked.connect(self.replace_header)
        button_layout.addWidget(self.replace_btn)

        self.undo_btn = QPushButton("撤销更改")
        self.undo_btn.clicked.connect(self.undo_changes)
        button_layout.addWidget(self.undo_btn)

        self.main_layout.addLayout(button_layout)

        # 主窗口设置
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择CSV文件夹")
        if folder_path:
            self.csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".csv")]
            self.current_index = -1
            self.navigate_file(1)  # 加载第一个文件

    def navigate_file(self, direction):
        if not self.csv_files:
            QMessageBox.warning(self, "警告", "请先加载一个文件夹！")
            return
        self.current_index += direction
        if 0 <= self.current_index < len(self.csv_files):
            file_path = self.csv_files[self.current_index]
            self.file_label.setText(f"当前文件: {os.path.basename(file_path)}")
            self.load_csv(file_path)
        else:
            self.current_index -= direction

    def jump_to_file(self):
        if not self.csv_files:
            QMessageBox.warning(self, "警告", "请先加载一个文件夹！")
            return
        try:
            index = int(self.index_input.text()) - 1
            if 0 <= index < len(self.csv_files):
                self.current_index = index
                self.navigate_file(0)
            else:
                QMessageBox.warning(self, "警告", "索引超出范围！")
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的索引！")

    def load_csv(self, file_path):
        try:
            self.current_data = pd.read_csv(file_path)
            self.backup_data = self.current_data.copy()
            self.display_headers()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法加载文件: {e}")

    def display_headers(self):
        if self.current_data is not None:
            headers = list(self.current_data.columns)

            # 表头展示
            self.header_table.setRowCount(1)
            self.header_table.setColumnCount(len(headers))
            self.header_table.setHorizontalHeaderLabels([f"列 {i+1}" for i in range(len(headers))])
            for col, header in enumerate(headers):
                item = QTableWidgetItem(header)
                item.setToolTip("原表头: " + header)
                self.header_table.setItem(0, col, item)

    def replace_header(self):
        if self.current_data is not None:
            try:
                new_headers = [
                    self.header_table.item(0, col).text() if self.header_table.item(0, col) else ""
                    for col in range(self.header_table.columnCount())
                ]
                if any(not header.strip() for header in new_headers):
                    QMessageBox.warning(self, "警告", "新表头不能为空！")
                    return
                self.current_data.columns = new_headers
                file_path = self.csv_files[self.current_index]
                self.current_data.to_csv(file_path, index=False)
                QMessageBox.information(self, "成功", "表头已成功替换！")
                self.display_headers()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"替换表头时出现问题: {e}")

    def undo_changes(self):
        if self.backup_data is not None:
            try:
                self.current_data = self.backup_data.copy()
                file_path = self.csv_files[self.current_index]
                self.current_data.to_csv(file_path, index=False)
                self.display_headers()
                QMessageBox.information(self, "成功", "已撤销更改！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"撤销更改时出现问题: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = CsvHeaderEditor()
    editor.show()
    sys.exit(app.exec_())
