import os
import csv
from collections import defaultdict
import chardet

def d_csv_utils(folder_path):
    """
    从指定文件夹中的所有 CSV 文件中提取列名信息，并将这些信息写入到一个新的 CSV 文件中。

    参数:
        folder_path (str): 包含 CSV 文件的文件夹路径。

    返回:
        None
    """
    # 使用 defaultdict 来存储列名及其出现的次数
    column_count = defaultdict(int)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否以.csv 结尾
        if filename.endswith('.csv'):
            # 构建文件的完整路径
            file_path = os.path.join(folder_path, filename)
            try:
                # 以二进制模式打开文件，检测其编码
                with open(file_path, 'rb') as file:
                    result = chardet.detect(file.read())
                    encoding = result['encoding']
                # 使用检测到的编码打开文件
                with open(file_path, mode='r', encoding=encoding, errors='ignore') as file:
                    # 创建 CSV 读取器
                    reader = csv.reader(file)
                    # 读取 CSV 文件的第一行，即列名
                    headers = next(reader)
                    # 遍历列名列表
                    for header in headers:
                        # 检查列名是否以 'C' 开头
                        if header and not header.startswith('C'):
                            # 统计列名出现的次数
                            column_count[header] += 1
            # 捕获读取文件时可能发生的异常
            except Exception as e:
                # 打印错误信息
                print(f"Error reading {file_path}: {e}")

    # 构建输出文件的路径
    output_path = './result/column_info.csv'
    # 以写入模式打开输出文件
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        # 创建 CSV 写入器
        writer = csv.writer(file)
        # 写入 CSV 文件的标题行
        writer.writerow(['Column Name', 'Count'])
        # 遍历列名及其出现次数的字典
        for column, count in sorted(column_count.items(), key=lambda item: item[1], reverse=True):
            # 将列名和出现次数写入 CSV 文件
            writer.writerow([column, count])

    # 打印一条信息，指示结果已保存到指定文件
    print(f"列名信息输出到 {output_path}")
