import os
import csv
from collections import defaultdict
import chardet

def d_csv_utils(folder_path):
    column_count = defaultdict(int)

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'rb') as file:
                    result = chardet.detect(file.read())
                    encoding = result['encoding']
                with open(file_path, mode='r', encoding=encoding, errors='ignore') as file:
                    reader = csv.reader(file)
                    headers = next(reader)
                    for header in headers:
                        if header and not header.startswith('C'):
                            column_count[header] += 1
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    output_path = './result/column_info.csv'
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Column Name', 'Count'])
        for column, count in sorted(column_count.items(), key=lambda item: item[1], reverse=True):
            writer.writerow([column, count])

    print(f"列名信息输出到 {output_path}")