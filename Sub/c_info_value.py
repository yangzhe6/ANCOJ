import pandas as pd

def c_info_value(csv_file, column_name):
    """
    从指定的 CSV 文件中提取某一列的所有唯一值，并将这些值打印出来。

    参数:
        csv_file (str): CSV 文件的路径。
        column_name (str): 要提取唯一值的列名。

    返回:
        None
    """
    # 读取 CSV 文件
    df = pd.read_csv(csv_file)
    # 检查列名是否存在
    if column_name in df.columns:
        # 提取唯一值
        unique_values = df[column_name].unique()
        # 将唯一值转换为字符串并连接成一个字符串
        values_as_string = '\n'.join(unique_values)
        # 打印列名和所有唯一值
        print(f"'{column_name}'列的所有值：")
        print(values_as_string + '\n')
    else:
        # 如果列名不存在，则打印错误信息
        print(f"CSV文件中没有找到'{column_name}'列。")

