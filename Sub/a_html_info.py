import os
import re
import chardet
import pandas as pd

def a_html_info(folder_path):
    results = pd.DataFrame(columns=[
        'id', 'Type', 'Dates', 'Observatory',
        'Reference Frame', 'Centre of Frame', 'Epoch of Equinox',
        'Time Scale', 'Reduction', 'Coordinates', 'Diffraction', 'Receptor',
        'Telescope', 'Observers', 'Relative To'
    ])

    status = {
        'success': [],
        'failures': {}
    }

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
                'Type': r'\btype:\s*(.+)',
                'Dates': r'\bdates:\s*(.+)',
                'Observatory': r'\bobservatory:\s*(.+)'
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
                    'Reference Frame': r'\breference frame:\s*(.+)',
                    'Centre of Frame': r'\bcentre of frame:\s*(.+)',
                    'Epoch of Equinox': r'\bepoch of equinox:\s*(.+)',
                    'Time Scale': r'\btime scale:\s*(.+)',
                    'Reduction': r'\breduction:\s*(.+)',
                    'Coordinates': r'\bcoordinates:\s*(.+)',
                    'Diffraction': r'\bdiff. refraction:\s*(.+)',
                    'Receptor': r'\breceptor:\s*(.+)',
                    'Telescope': r'\btelescope:\s*(.+)',
                    'Observers': r'\bobservers:\s*(.+)'
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
                    current_file_results['Relative To'] = '; '.join(relative_matches)

            else:
                if filename not in status['failures']:
                    status['failures'][filename] = []
                status['failures'][filename].append('Informations')

            results = results.append(current_file_results, ignore_index=True)

    output_path = './result/informations.csv'
    results.to_csv(output_path, index=False)

    print(f"成功提取 {len(status['success'])} 项到 {output_path} ")
    if status['failures']:
        print("失败的项有：")
        for filename, missing_keys in status['failures'].items():
            print(f"文件 {filename} 缺失以下信息：{', '.join(missing_keys)}")