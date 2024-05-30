"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

# Profile link: https://finance.yahoo.com/quote/AAL/profile/ with AAL name of stock

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import os
from datetime import datetime

def file_with_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

def get_response(url):
    response = requests.get(url, headers={'User-Agent': 'Custom'})
    if not response.ok:
        raise Exception(f'Failed to load page: {url}')
    return response

def get_page(url):
    response = get_response(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_results_number(soup):
    results = soup.find('span', class_='Mstart(15px) Fw(500) Fz(s)')
    return int(results.text.split()[2])

def get_table_header(soup, table_number=0):
    table = soup.find_all('table')[table_number]
    header = table.find_all('th')
    return [item.text for item in header]

def get_table_rows(soup, table_number=0):
    data = []
    table = soup.find_all('table')[table_number]
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = [ele.text.strip() for ele in row.find_all('td')]
        data.append([ele for ele in cols if ele])
    return data

def stock_tab_url(tab, symbol):
    return f'https://finance.yahoo.com/quote/{symbol}/{tab}?p={symbol}'

def read_profile(data, symbol):
    url = stock_tab_url('profile', symbol)
    soup = get_page(url)
    rows = get_table_rows(soup)
    ceo = rows[0]
    ceo = [0 if x == 'N/A' else x for x in ceo]
    data.loc[symbol, 'CEO Name'] = ceo[0]
    data.loc[symbol, 'CEO Year Born'] = int(ceo[4])
    div = soup.find('div', class_='Mb(25px)')
    info = [child.get_text(strip=True, separator='\n').splitlines() for child in div.find_all("p", recursive=False)]
    left, right = info
    data.loc[symbol, 'Country'] = left[-3]
    data.loc[symbol, 'Employees'] = int(right[-1].replace(',', '')) if right[-1] != ':' else 0

def read_statistics(data, symbol):
    url = stock_tab_url('statistics', symbol)
    soup = get_page(url)
    rows = get_table_rows(soup, 1)

def read_blackrock(data, symbol):
    url = stock_tab_url('holders', symbol)
    soup = get_page(url)
    headers = get_table_header(soup, 1)
    rows = get_table_rows(soup, 1)
    blackrock = next((row for row in rows if row[0] == 'Blackrock Inc.'), None)
    if blackrock:
        for x in [1, 4]:
            blackrock[x] = int(blackrock[x].replace(',', ''))
        blackrock[2] = datetime.strptime(blackrock[2], '%b %d, %Y')
        blackrock[3] = float(blackrock[3].strip('%')) / 100
        for field, value in zip(headers[1:], blackrock[1:]):
            data.loc[symbol, field] = value

def read_all_stocks(data, rows):
    for symbol, row in data.head(40).iterrows():
        read_profile(data, symbol)
        read_statistics(data, symbol)
        read_blackrock(data, symbol)

def pretty_sheet(title, data):
    pretty_table = tabulate(data.head(), headers='keys', tablefmt='pretty')
    length = len(pretty_table.splitlines()[0])
    title_formatted = title.center(length, '=')
    print(title_formatted)
    print(pretty_table)
    return title_formatted, pretty_table

def write_string(file, string_list):
    with open(file, 'w') as fp:
        fp.write('\n'.join(string_list))

def create_sheets(data):
    pretty_sheet(" all data ", data)
    title = ' 5 stocks with most youngest CEOs '
    table = data.nlargest(5, 'CEO Year Born')
    title, sheet = pretty_sheet(title, table[['Name', 'Country', 'Employees', 'CEO Name', 'CEO Year Born']])
    write_string(file_with_path('5stocks.txt'), [title, sheet])
    title = ' 10 largest holds of Blackrock Inc '
    table = data.nlargest(10, 'Value')
    title, sheet = pretty_sheet(title, table[['Name', 'Shares', 'Date Reported', '% Out', 'Value']])
    write_string(file_with_path('blackrock.txt'), [title, sheet])

def count_url(base_url, count, offset):
    return f'{base_url}?count={count}&offset={offset}'

def scrape_yahoo_most_active(url):
    data = pd.DataFrame()
    count = 100
    offset = 0
    url_offset = count_url(url, count, offset)
    soup = get_page(url_offset)
    res_num = get_results_number(soup)
    header = get_table_header(soup)
    rows = []
    while offset <= res_num:
        url_offset = count_url(url, count, offset)
        soup = get_page(url_offset)
        rows += get_table_rows(soup)
        offset += count
    data = pd.DataFrame([row[:2] for row in rows], columns=['Code', 'Name'])
    data = data.set_index('Code')
    read_all_stocks(data, rows)
    return data

url = 'https://finance.yahoo.com/most-active'
scraping = True
filename = file_with_path('output.csv')

if scraping:
    data = scrape_yahoo_most_active(url)
    data = data.fillna(0)
    data.Employees = data.Employees.astype(int)
    data['CEO Year Born'] = data['CEO Year Born'].astype(int)
    create_sheets(data)
    data.head().to_csv(filename, sep='\t', encoding='utf-8', na_rep='NULL')
