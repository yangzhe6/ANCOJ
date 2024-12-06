import os
import pandas as pd

def merge_csv_files(folder_path, output_file):
    # 获取文件夹中的所有CSV文件
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    # 初始化一个空的DataFrame来存储合并后的数据
    merged_df = pd.DataFrame()

    # 遍历每个CSV文件
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)

        # 确保所有DataFrame都有相同的列，缺失的列用NaN填充
        if not merged_df.empty:
            all_columns = set(merged_df.columns).union(set(df.columns))
            for col in all_columns:
                if col not in df.columns:
                    df[col] = pd.NA
                if col not in merged_df.columns:
                    merged_df[col] = pd.NA
        else:
            all_columns = set(df.columns)

        # 添加文件名和行号列
        df['文件名_行号'] = csv_file + '_' + df.index.astype(str)

        # 如果merged_df为空，则直接赋值
        if merged_df.empty:
            merged_df = df
        else:
            # 合并DataFrame，使用outer join以保证所有列都被保留
            merged_df = pd.concat([merged_df, df], axis=0, ignore_index=True, sort=False)

    # 将合并后的数据写入到输出文件中
    merged_df.to_csv(output_file, index=False)

folder_path = './Result/final'
output_file = './Result/merged.csv'

merge_csv_files(folder_path, output_file)
