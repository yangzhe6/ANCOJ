import sys
import os
import chardet
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QHBoxLayout
from PyQt5.Qt import QDesktopWidget

class FileViewer(QWidget):
    def __init__(self, files):
        super().__init__()
        self.files = [f for f in files if f.endswith('.html')]
        self.file_index_by_name = {os.path.splitext(f)[0]: idx for idx, f in enumerate(self.files)}
        self.current_file_index = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Viewer')
        
        available_geometry = QDesktopWidget().availableGeometry(self)
        screen_width = available_geometry.width()
        screen_height = available_geometry.height()

        self.setGeometry(10, 50, int(screen_width * 0.35), int(screen_height * 0.8))

        layout = QVBoxLayout()

        self.file_label = QLabel(self)
        self.file_label.setStyleSheet("font-weight: bold; color: darkred; font-size: 40px;")
        layout.addWidget(self.file_label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()

        self.goto_line_edit = QLineEdit(self)
        self.goto_line_edit.setPlaceholderText("输入文件名")
        self.goto_line_edit.returnPressed.connect(self.searchFile)
        btn_layout.addWidget(self.goto_line_edit)

        self.search_button = QPushButton('查询', self)
        self.search_button.clicked.connect(self.searchFile)
        btn_layout.addWidget(self.search_button)

        self.prev_button = QPushButton('前一页', self)
        self.prev_button.clicked.connect(self.prevFile)
        btn_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('后一页', self)
        self.next_button.clicked.connect(self.nextFile)
        btn_layout.addWidget(self.next_button)

        btn_layout.setStretchFactor(self.goto_line_edit, 1)
        btn_layout.setStretchFactor(self.search_button, 1)
        btn_layout.setStretchFactor(self.prev_button, 1)
        btn_layout.setStretchFactor(self.next_button, 1)

        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.show()
        self.loadFile(self.current_file_index)

    def loadFile(self, index):
        if 0 <= index < len(self.files):
            filename = self.files[index]
            filepath = os.path.join('./data/J', filename)
            try:
                with open(filepath, 'rb') as file:
                    raw_data = file.read()
                    encoding = chardet.detect(raw_data)['encoding']
                    file_content = raw_data.decode(encoding or 'utf-8', errors='replace')
                    format_start = file_content.find('Format.') + len('Format.')
                    if format_start > len('Format.'):
                        lines = file_content[format_start:].strip().split('\n')
                        first_line = '  ' + lines[0] if lines else ''
                        remaining_lines = '\n'.join(lines[1:])
                        self.text_edit.setText(first_line + '\n' + remaining_lines)
                    else:
                        self.text_edit.setText("No 'Format.' field found in file.")
                self.file_label.setText(os.path.splitext(filename)[0])
            except Exception as e:
                self.text_edit.setText(f"An error occurred: {e}")

    def prevFile(self):
        if self.current_file_index > 0:
            self.current_file_index -= 1
            self.loadFile(self.current_file_index)

    def nextFile(self):
        if self.current_file_index < len(self.files) - 1:
            self.current_file_index += 1
            self.loadFile(self.current_file_index)

    def searchFile(self):
        filename = self.goto_line_edit.text()
        if filename in self.file_index_by_name:
            self.current_file_index = self.file_index_by_name[filename]
            self.loadFile(self.current_file_index)
        else:
            self.text_edit.setText("File name not found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    files = [f for f in os.listdir('./data/J') if f.endswith('.html')]
    viewer = FileViewer(files)
    sys.exit(app.exec_())