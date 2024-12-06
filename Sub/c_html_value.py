import pandas as pd

def c_info_value(csv_file, column_name):
    df = pd.read_csv(csv_file)
    if column_name in df.columns:
        unique_values = df[column_name].unique()
        values_as_string = '\n'.join(unique_values)
        print(f"'{column_name}'列的所有值：")
        print(values_as_string + '\n')
    else:
        print(f"CSV文件中没有找到'{column_name}'列。")