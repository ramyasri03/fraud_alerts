import pandas as pd
import yaml

yaml_file=r"C:\Users\Ramya\OneDrive\gen_AI\file_storage.yml"
with open(yaml_file,'r',encoding='utf8') as ymlfile:
    cfg=yaml.safe_load(ymlfile)

input_folder=cfg['Fraud_alert_folder']
input_file = os.path.join(input_folder,cfg.get("fraud_alerts_log"))
output_file = os.path.join(input_folder,cfg.get("fraud_alerts_analysis.csv"))

df = pd.read_excel(input_file)

# Fields to analyze
fields = df.columns

# Prepare frequency lists with unique value count on top
freq_lists = {}
for field in fields:
    freq_dict = {}
    for val in df[field]:
        freq_dict[val] = freq_dict.get(val, 0) + 1
    
    freq_list = [f"{k} - {v}" for k, v in freq_dict.items()]
    unique_count = len(freq_dict)
    freq_list.insert(0, f"number of unique values - {unique_count}")
    freq_lists[field] = freq_list

# Pad all columns to same length with "None-0"
max_len = max(len(lst) for lst in freq_lists.values())
for field in freq_lists:
    while len(freq_lists[field]) < max_len:
        freq_lists[field].append("")

# Create DataFrame and save
analysis = pd.DataFrame(freq_lists)
analysis.to_csv(output_file, index=False)
