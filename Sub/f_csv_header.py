import sys
import os
import pandas as pd
import chardet
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLineEdit, QMessageBox, QTextEdit, QShortcut
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QKeySequence


class CsvHeaderEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Editor")
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()
        self.setGeometry(100, 100, int(screen_width * 0.35), int(screen_height * 0.8))
        self.csv_files = []
        self.file_names = []
        self.current_index = -1
        self.current_data = None
        self.html_viewer = None
        self.init_ui()
    def init_ui(self):
        self.main_layout = QVBoxLayout()
        
        # 创建一个水平布局来放置文件名标签和检索框
        file_label_layout = QHBoxLayout()
        self.file_label = QLabel("", self)
        self.file_label.setStyleSheet("font-weight: bold; color: darkred; font-size: 40px; margin: 0px;")
        self.file_label.setAlignment(Qt.AlignLeft)
        file_label_layout.addWidget(self.file_label)
        
        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("输入文件名")
        self.index_input.setFont(QFont("宋体", 12))
        self.index_input.returnPressed.connect(self.jump_to_file)
        file_label_layout.addWidget(self.index_input)
        
        # 将文件名标签和检索框的水平布局添加到主布局中
        self.main_layout.addLayout(file_label_layout)
        
        self.header_table = QTableWidget()
        self.header_table.setStyleSheet(
            """
            QTableWidget {
                font-family: '宋体'; /* 设置字体类型为宋体 */
                font-size: 30px; /* 设置字体大小 */
                text-align: center;  /* 设置单元格文本居中 */
            }
            """
        )
        
        self.header_table.horizontalHeader().setStretchLastSection(True)
        self.header_table.verticalHeader().setVisible(True)
        self.header_table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.header_table.cellChanged.connect(self.on_cell_changed)
        self.main_layout.addWidget(self.header_table)
        
        button_layout = QHBoxLayout()
        button_font = QFont("宋体", 15)  # 设置按钮字体和大小
        self.load_csv_folder_btn = QPushButton("CSV")
        self.load_csv_folder_btn.setFont(button_font)
        self.load_csv_folder_btn.setFixedHeight(50)
        self.load_csv_folder_btn.clicked.connect(self.load_csv_folder)
        button_layout.addWidget(self.load_csv_folder_btn)
        
        self.load_html_folder_btn = QPushButton("HTML")
        self.load_html_folder_btn.setFont(button_font)
        self.load_html_folder_btn.setFixedHeight(50)
        self.load_html_folder_btn.clicked.connect(self.load_html_folder)
        button_layout.addWidget(self.load_html_folder_btn)
        
        self.prev_file_btn = QPushButton("上一页")
        self.prev_file_btn.setFont(button_font)
        self.prev_file_btn.setFixedHeight(50)
        self.prev_file_btn.clicked.connect(lambda: self.navigate_file(-1))
        button_layout.addWidget(self.prev_file_btn)
        
        self.next_file_btn = QPushButton("下一页")
        self.next_file_btn.setFont(button_font)
        self.next_file_btn.setFixedHeight(50)
        self.next_file_btn.clicked.connect(lambda: self.navigate_file(1))
        button_layout.addWidget(self.next_file_btn)
        self.next_shortcut = QShortcut(QKeySequence("F3"), self)
        self.next_shortcut.activated.connect(lambda: self.navigate_file(1))

        
        self.replace_btn = QPushButton("替换")
        self.replace_btn.setFont(button_font)
        self.replace_btn.setFixedHeight(50)
        self.replace_btn.clicked.connect(self.replace_header)
        button_layout.addWidget(self.replace_btn)
        self.replace_shortcut = QShortcut(QKeySequence("F2"), self)
        self.replace_shortcut.activated.connect(self.replace_header)
        self.main_layout.addLayout(button_layout)

        
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)


       

    # 以下是其他方法的实现，包括加载CSV文件夹、加载HTML文件夹、导航文件、跳转到文件、加载CSV文件、显示表头、替换表头、单元格改变事件处理、同步文件索引、显示信息、警告和错误消息等。
    def load_csv_folder(self):
        csv_folder_path = QFileDialog.getExistingDirectory(self, "选择CSV文件夹")
        if csv_folder_path:
            self.csv_files = [os.path.join(csv_folder_path, f) for f in os.listdir(csv_folder_path) if f.endswith(".csv")]
            self.file_names = [os.path.splitext(os.path.basename(f))[0] for f in self.csv_files]
            self.current_index = -1
            self.navigate_file(1)

    def load_html_folder(self):
        html_folder_path = QFileDialog.getExistingDirectory(self, "选择HTML文件夹")
        if html_folder_path:
            if not self.html_viewer:
                self.html_viewer = HtmlViewer(html_folder_path, self)
                self.html_viewer.show()
            else:
                self.html_viewer.load_folder(html_folder_path)

    def navigate_file(self, direction):
        if not self.csv_files:
            self.show_warning("警告", "请先加载CSV文件夹！")
            return
        self.current_index += direction
        if 0 <= self.current_index < len(self.csv_files):
            file_path = self.csv_files[self.current_index]
            file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
            self.file_label.setText(f"{file_name_without_extension}")
            self.load_csv(file_path)
            self.sync_file_index(self.current_index)
        else:
            self.current_index -= direction

    def jump_to_file(self):
        if not self.csv_files:
            self.show_warning("警告", "请先加载CSV文件夹！")
            return
        input_name = self.index_input.text().strip()
        if input_name in self.file_names:
            self.current_index = self.file_names.index(input_name)
            self.navigate_file(0)
            # 同步HTML文件索引
            if self.html_viewer:
                self.html_viewer.loadFileByName(input_name + '.html')  # 确保传递完整的文件名
        else:
            self.show_warning("警告", "文件名不存在，请检查输入！")

    def load_csv(self, file_path):
        try:
            self.current_data = pd.read_csv(file_path)
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
                
                if self.html_viewer:
                    self.html_viewer.nextFile()
                self.navigate_file(1)
            except Exception as e:
                self.show_critical("错误", f"替换表头时出现问题: {e}")


    def on_cell_changed(self, row, col):
        next_row = row + 1
        if next_row < self.header_table.rowCount():
            self.header_table.setCurrentCell(next_row, col)

    def sync_file_index(self, csv_index):
        if self.html_viewer and 0 <= csv_index < len(self.csv_files):
            html_file_name = os.path.splitext(os.path.basename(self.csv_files[csv_index]))[0] + '.html'
            html_index = next((i for i, f in enumerate(self.html_viewer.html_files) if os.path.splitext(os.path.basename(f))[0] == html_file_name), None)
            if html_index is not None:
                self.html_viewer.current_index = html_index
                self.html_viewer.loadFile(self.html_viewer.current_index)

    def show_information(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.show()
        QTimer.singleShot(300, msg_box.close)  # 0.3秒后关闭提示框

    def show_warning(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.show()
        QTimer.singleShot(300, msg_box.close)  # 0.3秒后关闭提示框

    def show_critical(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.show()
        QTimer.singleShot(300, msg_box.close)  # 0.3秒后关闭提示框
class HtmlViewer(QWidget):
    def __init__(self, folder_path, csv_editor):
        super().__init__()
        self.setWindowTitle("HTML Viewer")
        self.csv_editor = csv_editor
        self.folder_path = folder_path
        self.html_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".html")]
        self.current_index = 0
        self.initUI()

    def initUI(self):
        available_geometry = QApplication.desktop().screenGeometry(self)
        screen_width = available_geometry.width()
        screen_height = available_geometry.height()
        self.setGeometry(100+int(screen_width * 0.35), 100, int(screen_width * 0.35), int(screen_height * 0.8))

        layout = QVBoxLayout()
        self.file_label = QLabel(self)
        self.file_label.setStyleSheet("font-weight: bold; color: darkred; font-size: 40px;")
        layout.addWidget(self.file_label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        button_font = QFont("宋体", 15)  # 设置按钮字体和大小
        self.prev_button = QPushButton('上一页', self)
        self.prev_button.setFont(button_font)
        self.prev_button.setFixedHeight(50)
        self.prev_button.clicked.connect(self.prevFile)
        btn_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('下一页', self)
        self.next_button.setFont(button_font)
        self.next_button.setFixedHeight(50)
        self.next_button.clicked.connect(self.nextFile)
        btn_layout.addWidget(self.next_button)

        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.show()
        self.loadFile(self.current_index)

    # 以下是其他方法的实现，包括加载文件夹、加载文件、前后翻页等。
    def load_folder(self, folder_path):
        self.folder_path = folder_path
        self.html_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".html")]
        self.current_index = 0  # 重置当前索引
        self.loadFile(self.current_index)


    def loadFile(self, index):
        if 0 <= index < len(self.html_files):
            filename = self.html_files[index]
            filepath = filename  # 直接使用filename，因为它已经是完整的路径
            try:
                with open(filepath, 'rb') as file:
                    raw_data = file.read()
                    encoding = chardet.detect(raw_data)['encoding']
                    file_content = raw_data.decode(encoding or 'utf-8', errors='replace')
                    # 查找"Format."的位置并截取之后的内容
                    format_start = file_content.find('Format.')
                    if format_start != -1:
                        format_start += len('Format.')
                        lines = file_content[format_start:].strip().split('\n')
                        # 只在第一行添加两个空格
                        first_line = '  ' + lines[0] if lines else ''
                        remaining_lines = '\n'.join(lines[1:])
                        updated_content = first_line + '\n' + remaining_lines
                        self.text_edit.setText(updated_content)
                    else:
                        self.text_edit.setText("No 'Format.' field found in file.")
                self.file_label.setText(os.path.splitext(os.path.basename(filename))[0])
            except Exception as e:
                self.text_edit.setText(f"An error occurred: {e}")

    def loadFileByName(self, file_name):
        # 移除文件扩展名，因为我们保存的是不带扩展名的文件名
        base_name = os.path.splitext(file_name)[0]
        # 找到同名的HTML文件的索引
        html_index = next((i for i, f in enumerate(self.html_files) if os.path.splitext(os.path.basename(f))[0] == base_name), None)
        if html_index is not None:
            self.current_index = html_index
            self.loadFile(self.current_index)
        else:
            self.text_edit.setText("File not found.")

    def prevFile(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.loadFile(self.current_index)

    def nextFile(self):
        if self.current_index < len(self.html_files) - 1:
            self.current_index += 1
            self.loadFile(self.current_index)

# 以下是主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = CsvHeaderEditor()
    editor.show()
    sys.exit(app.exec_())
