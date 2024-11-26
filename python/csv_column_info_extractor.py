import os
import csv

def extract_csv_column_info(csv_path, output_file='./result/column_info.csv'):
    csv_info = []
    csv_files = [f for f in os.listdir(csv_path) if f.endswith(".csv")]
    for filename in csv_files:
        file_path = os.path.join(csv_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                first_row = next(csv_reader)
                num_columns = len(first_row)
                csv_info.append([filename.split(".")[0], num_columns])
        except Exception as e:
            print(f"读取{filename}失败: {e}")

    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['文件名', '列数'])
            for info in csv_info:
                writer.writerow(info)
        print("列信息已写入")
    except Exception as e:
        print(f"写入{output_file}失败: {e}")
