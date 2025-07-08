import pandas as pd
import os
import yaml

yaml_file=r"C:\Users\Ramya\OneDrive\gen_AI\file_storage.yml"
with open(yaml_file,'r',encoding='utf8') as ymlfile:
    cfg=yaml.safe_load(ymlfile)

input_folder=cfg['Fraud_alert_folder']
input_path = os.path.join(input_folder,cfg.get("fraud_alerts_log"))
alert_reason = os.path.join(input_folder,cfg.get("alert_reason"))
output_path = os.path.join(input_folder,cfg.get("fraud_alerts_statment"))

alerts_df=pd.read_excel(alert_reason)
alerts_reason_dic=pd.Series(alerts_df['Reasons'].values,index=alerts_df['Alerts']).to_dict()
result=[]

df=pd.read_excel(input_path)
result=[]

for index,row in df.iterrows():
    row_dict=row.to_dict()
    result.append(f"Instruction: Generate a user friendly explanation of the fraud alert reason given in the Input based on the card number, expiration date, amount, merchant, email id, location and IP address. Input : Card Number is {row_dict['CardNumber']} , Expiration Date is {row_dict['ExpirationDate']} , Amount is {row_dict['AmountUSD']} , Merchant is {row_dict['MerchantName']} , Email ID is {row_dict['EmailID']} , Location is {row_dict['Location']} , IP address is {row_dict['IP']} , Fraud alert reason is {row_dict['FraudAlertReason']}. Output : The Trasaction seems suspicious {alerts_reason_dic[row_dict['FraudAlertReason']]}")

dff=pd.DataFrame(result)
dff.to_excel(output_path,index=False)
print(f"file saves{output_path}")