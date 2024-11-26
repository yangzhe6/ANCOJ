import os
import re
import chardet
import pandas as pd

def extract_astronomy_data(folder_path):
    results = pd.DataFrame(columns=[
        'id', '类型', '日期', '天文台', 
        '参考框架', '框架中心', '坐标系统', 
        '时间尺度', '归算', '坐标', '衍射', '接收器', 
        '望远镜', '观测者', '相对'
    ])
    status = {'success': [], 'failures': {}}
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            file_id = os.path.splitext(filename)[0]
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
            with open(file_path, 'r', encoding=encoding) as file:
                html_content = file.read()
            current_file_results = {'id': file_id}
            contents_patterns = {
                '类型': r'\btype:\s*(.+)',
                '日期': r'\bdates:\s*(.+)',
                '天文台': r'\bobservatory:\s*(.+)'
            }
            for key, pattern in contents_patterns.items():
                regex = re.compile(pattern)
                match = regex.search(html_content)
                if match:
                    current_file_results[key] = match.group(1).strip()
                    status['success'].append(filename)
                else:
                    if filename not in status['failures']:
                        status['failures'][filename] = []
                    status['failures'][filename].append(key)
            informations_pattern = r'Informations\..*?(?=\b(Comments|Format)\.)'
            informations_match = re.search(informations_pattern, html_content, re.DOTALL)
            if informations_match:
                informations_content = informations_match.group(0).strip()
                fields_patterns = {
                    '参考框架': r'\breference frame:\s*(.+)',
                    '框架中心': r'\bcentre of frame:\s*(.+)',
                    '分点历元': r'\bepoch of equinox:\s*(.+)',
                    '时间尺度': r'\btime scale:\s*(.+)',
                    '归算': r'\breduction:\s*(.+)',
                    '坐标': r'\bcoordinates:\s*(.+)',
                    '衍射': r'\bdiff. refraction:\s*(.+)',
                    '接收器': r'\breceptor:\s*(.+)',
                    '望远镜': r'\btelescope:\s*(.+)',
                    '观测者': r'\bobservers:\s*(.+)'
                }
                for field, pattern in fields_patterns.items():
                    regex = re.compile(pattern)
                    match = regex.search(informations_content)
                    if match:
                        current_file_results[field] = match.group(1).strip()
                    else:
                        current_file_results[field] = None
                relative_pattern = r'\brelative to:\s*(.+)'
                relative_matches = re.findall(relative_pattern, informations_content)
                if relative_matches:
                    current_file_results['相对'] = '; '.join(relative_matches)
            else:
                if filename not in status['failures']:
                    status['failures'][filename] = []
                status['failures'][filename].append('Informations')
            results = results.append(current_file_results, ignore_index=True)
    results.to_csv('./result/Informations.csv', index=False)
    print(f"成功提取 {len(status['success'])} 项")
    if status['failures']:
        print("失败的项有：")
        for filename, missing_keys in status['failures'].items():
            print(f"文件 {filename} 缺失以下信息：{', '.join(missing_keys)}")
