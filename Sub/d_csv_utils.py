import os
import csv
from collections import defaultdict
import chardet

def d_csv_utils(folder_path, sort_by='count'):
    column_count = defaultdict(int)
    column_files = defaultdict(list)

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                # 自动检测文件编码
                with open(file_path, 'rb') as file:
                    result = chardet.detect(file.read())
                    encoding = result['encoding']
                
                # 读取 CSV 文件
                with open(file_path, mode='r', encoding=encoding, errors='ignore') as file:
                    reader = csv.reader(file)
                    headers = next(reader)
                    for header in headers:
                        if header:  # 确保列名非空
                            column_count[header] += 1
                            column_files[header].append(os.path.splitext(filename)[0])  # 去掉文件后缀
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # 创建输出目录
    output_path = './result/column_info.csv'

    # 确定排序方式
    if sort_by == 'name':
        sorted_columns = sorted(column_count.items(), key=lambda item: item[0])
    else:  # 默认按统计次数排序
        sorted_columns = sorted(column_count.items(), key=lambda item: item[1], reverse=True)

    # 写入统计结果
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Column Name', 'Count', 'Files'])
        for column, count in sorted_columns:
            # 对于出现次数少于10的列，记录文件名
            files = "; ".join(column_files[column]) if count < 10 else ""
            writer.writerow([column, count, files])

    print(f"列名信息输出到 {output_path}")
