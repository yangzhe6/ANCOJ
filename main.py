from Sub.a_html_info import a_html_info
from Sub.b_csv_convert import b_convert_csv
from Sub.c_html_value import c_info_value
from Sub.d_csv_utils import d_csv_utils
from Sub.e_csv_errror import e_errror_info
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(a, b, c, d, e):
    if a:
        logging.info('提取天文数据...')
        a_html_info(folder_path)
    if b:
        logging.info('将TXT文件夹中的文件转换为CSV...')
        b_convert_csv(folder_path, csv_path)
    if c:
        logging.info('打印CSV文件中指定列的所有唯一值...')
        c_info_value(result_path + '/Informations.csv', 'Epoch of Equinox')
        c_info_value(result_path + '/Informations.csv', 'Time Scale')
    if d:
        logging.info('提取CSV文件的列名信息...')
        d_csv_utils(result_path+'/final', sort_by=' ')
    if e:
        logging.info('检测CSV文件的错误信息...')
        e_errror_info(csv_path)

if __name__ == '__main__':
    folder_path = './Data/J'
    result_path = './Result'
    csv_path = './Result/csv'
    main(a=False, b=False, c=True, d=False, e=False)

