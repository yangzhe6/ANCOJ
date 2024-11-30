import os
import pandas as pd

def detect_csv_errors(folder_path, output_file="error_report.csv"):
    """
    检测指定文件夹中的CSV文件错误，并将结果保存到CSV文件中。
    
    :param folder_path: 要检测的CSV文件夹路径
    :param output_file: 错误报告CSV文件的名称
    """
    if not os.path.exists(folder_path):
        print("指定的文件夹不存在！")
        return

    # 获取文件夹中所有CSV文件
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not csv_files:
        print("指定文件夹中没有CSV文件！")
        return

    errors = []  # 存储错误信息，每条记录是一个字典

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        try:
            # 尝试读取CSV文件
            data = pd.read_csv(file_path)
        except Exception as e:
            errors.append({"文件名": file_name, "错误信息": f"文件读取错误 - {e}"})
            continue

        # 检查表头完整性
        headers = list(data.columns)
        if any(h.strip() == "" for h in headers):
            errors.append({"文件名": file_name, "错误信息": "表头中存在空列名"})

        # 检查行列一致性
        for i, row in enumerate(data.itertuples(index=False, name=None)):
            if len(row) != len(headers):
                errors.append({
                    "文件名": file_name,
                    "错误信息": f"第{i + 1}行的列数({len(row)})与表头列数({len(headers)})不一致"
                })

        # 检查空值列
        empty_threshold = 0.5  # 空值比例阈值
        empty_columns = data.isnull().mean()
        for col_name, empty_ratio in empty_columns.items():
            if empty_ratio > empty_threshold:
                errors.append({
                    "文件名": file_name,
                    "错误信息": f"列 '{col_name}' 空值比例过高 ({empty_ratio:.1%})"
                })

    # 将错误信息写入CSV文件
    if errors:
        error_df = pd.DataFrame(errors)
        error_df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"检测完成！错误报告已保存到 '{output_file}'")
    else:
        print("检测完成！未发现错误。")

if __name__ == "__main__":
    folder = input("请输入要检测的CSV文件夹路径：")
    detect_csv_errors(folder)
