import sys
import re
import numpy as np
import pandas as pd
import openpyxl

SB2CS_TYPES = {
    'Deposit': 'deposit',
    'Withdrawal': 'withdrawal',
    'Earnings': 'interest_earn',
    'Sell': 'sell',
    'Buy': 'buy',
}

SOURCE_FILE = sys.argv[1]

def get_base_currency(source):
    wb = openpyxl.load_workbook(filename = source)
    return wb.active['B4'].value

BASE_CURRENCY = get_base_currency(SOURCE_FILE)

def find_exchange_pair(note):
    PAIR_PATTERN_FROM = r"Exchanged from (\d*.?\d*) ([a-zA-Z]+)$"
    PAIR_PATTERN_TO = r"Exchanged to (\d*.?\d*) ([a-zA-Z]+)"
    if note is np.nan:
        return (0.0, note)
    match = re.search(PAIR_PATTERN_FROM, note)
    if match:
        return (float(match.group(1)), match.group(2))
    match = re.search(PAIR_PATTERN_TO, note)
    if match:
        return (float(match.group(1)), match.group(2))
    return (0.0, np.nan)

def calculate_price(row):
    value = find_exchange_pair(row['Note'])[0]
    if value == 0.0:
        return np.nan
    else:
        return value / row['Net amount']
    
def calculate_fee(row):
    if row['Fee'] != 0.0:
        return 100 * row['Fee'] / row['Gross amount']
    if row[f'Fee ({BASE_CURRENCY})'] != 0.0:
        return 100 * row[f'Fee ({BASE_CURRENCY})'] / row[f'Gross amount ({BASE_CURRENCY})']
    return 0.0

def convert(source, destination):
    try:
        sb = pd.read_excel(source, skiprows=8, engine='openpyxl')
    except Exception as e:
        print("Cannot read input file.")
        raise e
    sb['Price'] = sb.apply(calculate_price, axis=1)
    sb['Exchange'] = 'SwissBorg'
    sb['Pair'] = sb['Note'].apply(lambda _: find_exchange_pair(_)[1])
    sb['Type'] = sb['Type'].apply(lambda _: SB2CS_TYPES[_])
    sb['Fee (percent)'] = sb.apply(calculate_fee, axis=1)
    sb.drop('Fee', axis=1, inplace=True)
    sb.drop(f'Fee ({BASE_CURRENCY})', axis=1, inplace=True)
    sb.drop('Local time', axis=1, inplace=True)
    sb.drop(f'Net amount ({BASE_CURRENCY})', axis=1, inplace=True)
    sb.drop('Gross amount', axis=1, inplace=True)
    sb.drop(f'Gross amount ({BASE_CURRENCY})', axis=1, inplace=True)
    sb.rename(columns={'Currency': 'Coin Symbol', 'Time in UTC': 'Date', 'Note': 'Notes', 'Fee (percent)': 'Fee', 'Net amount': 'Amount'}, inplace=True)
    sb = sb[['Coin Symbol', 'Exchange', 'Pair', 'Type', 'Amount', 'Price', 'Fee', 'Date', 'Notes']]
    sb = sb[sb['Type'] != 'sell']
    sb.to_csv(destination)
    return sb
    
if __name__ == '__main__':
    convert(SOURCE_FILE, sys.argv[2])
