import os
import chardet
import csv
import re
from tqdm import tqdm

def b_convert_csv(folder_path, csv_path):
    """
    将指定文件夹中的所有 TXT 文件转换为 CSV 文件，并将这些 CSV 文件保存到另一个指定的文件夹中。

    参数:
        folder_path (str): 包含 TXT 文件的文件夹路径。
        csv_path (str): 保存 CSV 文件的文件夹路径。

    返回:
        None
    """
    # 如果 CSV 文件夹不存在，则创建它
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    def detect_encoding(file_path):
        """
        检测文件的编码格式。

        参数:
            file_path (str): 文件的路径。

        返回:
            str: 文件的编码格式。
        """
        with open(file_path, 'rb') as file:
            return chardet.detect(file.read())['encoding']

    def detect_delimiter(file_content):
        """
        检测文件内容中的分隔符。

        参数:
            file_content (str): 文件的内容。

        返回:
            str: 检测到的分隔符。
        """
        patterns = {',': re.compile(r'[^,]+'), '\t': re.compile(r'[^\t]+'), ' ': re.compile(r'[^\s]+')}
        max_match_count = 0
        detected_delimiter = None
        for delimiter, pattern in patterns.items():
            matches = len(pattern.findall(file_content))
            if matches > max_match_count:
                max_match_count = matches
                detected_delimiter = delimiter
        return detected_delimiter

    failed_files = []

    # 获取所有以.txt 结尾的文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    # 遍历所有 TXT 文件
    for filename in tqdm(txt_files, desc='处理TXT文件'):
        file_path = os.path.join(folder_path, filename)
        # 检测文件编码
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
            file_content = file.read()
            # 检测文件分隔符
            delimiter = detect_delimiter(file_content)
            if delimiter is None:
                # 如果未检测到分隔符，则将文件名添加到失败文件列表中
                failed_files.append(filename)
                continue
            lines = file_content.split('\n')
            csv_lines = []
            for line in lines:
                if line.strip():
                    if delimiter == '\t':
                        fields = line.split('\t')
                    elif delimiter == ' ':
                        fields = line.split()
                    else:
                        fields = line.split(',')
                    # 为每个字段添加方括号
                    fields_with_brackets = [f"[{field}]" for field in fields]
                    csv_lines.append(fields_with_brackets)
        # 生成 CSV 文件名
        csv_filename = filename.replace('.txt', '.csv')
        csv_file_path = os.path.join(csv_path, csv_filename)
        try:
            # 将 CSV 内容写入文件
            with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # 写入 CSV 文件的标题行
                headers = [f"C{i+1}" for i in range(len(csv_lines[0]))]
                csv_writer.writerow(headers)
                for row in csv_lines:
                    csv_writer.writerow(row)
        except Exception as e:
            # 如果写入失败，则将文件名添加到失败文件列表中
            failed_files.append(filename)
            print(f"写入{filename}失败: {e}")

    if failed_files:
        print("转换失败的文件:", failed_files)
    else:
        print("所有文件转换成功。")
