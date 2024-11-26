# 导入模块
from python.txt_to_csv_converter import convert_txt_to_csv
from python.csv_column_info_extractor import extract_csv_column_info
from python.csv_value_extractor import extract_unique_values
from python.astronomy_data_extractor import extract_astronomy_data

# 设置文件路径
folder_path = './data/J'  # 原始数据目录
result_path = './result'  # 结果生成目录
csv_path = './result/csv'  # CSV文件目录

# # 提取天文数据
# print('\n提取天文数据...')
# extract_astronomy_data(folder_path)

# # 将TXT文件夹中的文件转换为CSV
# print('将TXT文件夹中的文件转换为CSV...')
# convert_txt_to_csv(folder_path, csv_path)


# # 提取CSV文件的列信息
# print('提取CSV文件的列信息...')
# extract_csv_column_info(csv_path)


# # 打印CSV文件中指定列的所有唯一值（示例代码，可根据需要取消注释）
# print('打印CSV文件中指定列的所有唯一值...')
# extract_unique_values(result_path + '/Informations.csv', '坐标系统')
# extract_unique_values(result_path + '/Informations.csv', '时间尺度')

