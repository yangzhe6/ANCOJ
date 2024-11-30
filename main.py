from Sub.a_html_info import a_html_info
from Sub.b_convert_csv import b_convert_csv
from Sub.c_info_value import c_info_value
from Sub.d_csv_utils import d_csv_utils

def main(a,b,c,d):
    if a :
        print('\n提取天文数据...\n')
        a_html_info(folder_path)
    if b :
        print('\n将TXT文件夹中的文件转换为CSV...\n')
        b_convert_csv(folder_path, csv_path)
    if c :
        print('\n打印CSV文件中指定列的所有唯一值...\n')
        c_info_value(result_path + '/Informations.csv', 'Epoch of Equinox')
        c_info_value(result_path + '/Informations.csv', 'Time Scale')
    if d :
        print('\n提取CSV文件的列名信息...\n')
        d_csv_utils(result_path+'/final')

if __name__ == '__main__':
    # 设置文件路径
    folder_path = './Data/J'
    result_path = './Result'
    csv_path = './Result/csv'
    main(0,1,0,1)