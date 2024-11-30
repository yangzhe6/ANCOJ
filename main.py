from Sub.a_html_info import a_html_info
from Sub.b_convert_csv import b_convert_csv
from Sub.c_info_value import c_info_value
from Sub.d_csv_utils import d_csv_utils

def main(a,b,c,d):
    if a == 1:
        print('\n提取天文数据...\n')
        a_html_info(folder_path)
    if b == 1:
        print('\n将TXT文件夹中的文件转换为CSV...\n')
        b_convert_csv(folder_path, csv_path)
    if c == 1:
        print('\n打印CSV文件中指定列的所有唯一值...\n')
        c_info_value(result_path + '/Informations.csv', 'Epoch of Equinox')
        c_info_value(result_path + '/Informations.csv', 'Time Scale')
    if d == 1:
        print('\n提取CSV文件的列名信息...\n')
        d_csv_utils(result_path+'/final')

if __name__ == '__main__':
    # 设置文件路径
    folder_path = './Data/J'  # 原始目录
    result_path = './Result'  # 结果目录
    csv_path = './Result/csv'  # CSV文件目录
    main(0,0,0,1)