import openai
from openai import OpenAI
import pandas as pd
import re
import os
import random
import yaml
import string
from config import API_KEY,API_KEY_URL,MODEL

yaml_file=r"C:\Users\Ramya\OneDrive\gen_AI\file_storage.yml"
with open(yaml_file,'r',encoding='utf8') as ymlfile:
    cfg=yaml.safe_load(ymlfile)

input_folder=cfg['Fraud_alert_folder']

client=OpenAI(
    api_key=API_KEY,
    base_url=API_KEY_URL
)

response = client.chat.completions.create(
    model=MODEL,
    n=1,
    messages=[
        {"role":"system",
        "content":"You are an AI assistant who can find credit card fraud alerts and log."},
        {
            "role": "user",
            "content": """ generate exactly **1000 rows** of synthetic data. Each row must contain 9 values, separated by '|', representing the following columns in exact order:
CardHolderid | CardNumber | Expirationdate | transaction | amtusd | name | Emailid | location | IP | alerts | risk  | status

you are creating data for 12 columns.
make sure the result followed the exact column order as i given the above.

    1.CardHolderid : make sure CardHolderid is alpha numeric with 5 digits. first 2 digit is Alphabet with captial case
    next 3 digit is random number.ensure the fomat like 'CH001','AK239','MK920'
    2.CardNumber : make sure CardNumber is masked values example (xxxx-xxxx-xxxx-6789) only last 4 digit visibles
    those 4 digit is random number. ensure the fomat like 'xxxx-xxxx-xxxx-3435','xxxx-xxxx-xxxx-0023'
    3.Expirationdate : generate random expiration date with the format oF 'MM/YYYY'.ensure the generated month and year(expirationdate) is after the current MM/YYYY(June/2025)
    4.transaction : creating random transaction type and make sure the transaction type only realted to bank transaction type like('Online','In store','POS','Wallet','Telephone','ATM','Subscription')
    5.amtusd : if the alert is 'high amount' or 'large Amount' - amtusd is between 10000 to 20000. 
               otherwise create a random float values for amtusd under 1000.
    ensure its a both float or interger values and ensure if its a float then after the '.' only 2 or 3 digit is enough.
    6.name : make sure your mechand name is company names. ensure the name is in united kingdom (UK).
    7.Emailid : Generate random email id.make sure its unique
    8.location : location should be UK cities with the format of ('South Stuart, UK','Carlberg, UK')
    9.IP : generate random ip id.
    10.alerts : generate a random alerts from the list .("Abnormal spending pattern","Compromised card",
    "Fake email addresses","Foreign IP","Foreign location","High amount","Incorrect expiration dates",
    "Low value foreign","Mismatched billing address","Multiple shipping addresses on one card",
    "No shopping history","Suspicious IP address","Suspicious zero amount attempt","High risk merchant")
    11.risk : to create a random values. the number range is 0-99.
    12.status : create a random status and make sure random status is only related to bank credit alert status like 'Investigating','Resolved','Dismissed','Cleared'. those are only model example. you should create random status related to bank creadit alert status.

important logic:
make sure 1000 rows 12 columns is generated.
if alerts in 'Hight amount' then amtusd is must between 10000 to 20000
if alerts in 'Foreign ip' or 'Foreign location' then location is USA,Africa,UAE,Italy,Finland and Australia cities and not UK cities with the format of ('Lagos, Nigeria','New York, USA')
if alerts in 'Incorrect expiration dates' then the Expiration date should be before the current date(June,2025).
if alerts in 'Low value foreign' then the location should be other than UK cities and amtusd is less than 10.
if alerts in 'Suspicious IP address' then the IP should be from this list (192.0.2.1, 104.135.196.55, 104.248.169.251, 107.189.8.238, 134.238.184.178, 136.226.102.90, 185.220.100.240, 185.220.101.7, 192.42.116.198, 72.217.36.105, 107.189.8.56).
if alerts in 'Suspicious zero amount attempt' then amtusd should be 0.
if alerts in 'High risk merchant' then the name should be from the list (Prestige Poker Network,SkyHigh Betting Corp,Luxury Tech Resale,NextGen Forex Solutions,HighRisk Tech Gadgets,FastTrack Loan Services,Dragon Den Crypto Investments,CrytoVault Traders,Platinum Debt Solutions,Titanic Tours and Travels).
ensure there is no None/empty values and Return the result table using '|' as column separators and without header.and without unnessasy words like 'markdown'.make sure its followed the column order.
here sample output format  : CH123 | xxx-xxx-xxx-1234 | etc....
                             CH212 | xxx-xxx-xxx-2243 | etc.... """
        }
    ]
)


def generate_alert_ids():
    return [f"AL{str(i).zfill(4)}" for i in range(10000)]

def generate_trans_ids():
    trans_ids = set()
    while len(trans_ids) < 10000:
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=3))
        trans_ids.add(letters + digits)
    return list(trans_ids)

# total_rows_needed = 1000
all_rows = []
total_rows_needed = 10000

while len(all_rows) < total_rows_needed:
    responses=response.choices[0].message
    rows = [re.split(r"\s*\|\s*", line.strip()) for line in responses.content.strip().splitlines()]
    # filter for rows with exactly 10 columns and unique keys
    valid_rows = [row for row in rows if len(row) == 12]
    all_rows.extend(valid_rows)
    print(f"Collected {len(all_rows)} rows so far...")
# Trim to exact total_rows_needed if exceeded
all_rows = all_rows[:total_rows_needed]

# Create dataframe
df = pd.DataFrame(all_rows, columns=[
    'CardHolderId', 'CardNumber', 'ExpirationDate','TransactionChannel', 'AmountUSD', 
    'MerchantName','EmailID' ,'Location','IP' ,'FraudAlertReason', 'RiskScore', 'Status'
])
df.insert(0,'AlertID',generate_alert_ids())
df.insert(4, 'TransactionID', generate_trans_ids())


# Save to Excel
excel_path = os.path.join(input_folder,cfg.get("fraud_alerts_log"))
df.to_excel(excel_path, index=False)

# Print confirmation and preview
print("✅ Excel file created:", excel_path)
print(df)
