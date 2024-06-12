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

import ssl
from bs4 import BeautifulSoup
import requests
from http import cookiejar
import random

ssl._create_default_https_context = ssl._create_stdlib_context

user_agent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
]


class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


def make_request(url: str) -> tuple[int, bytes]:
    req = requests.get(url, headers={'User-Agent': random.choice(user_agent)}, timeout=5)
    if req.status_code == 200:
        return 200, req.content
    else:
        print("Make request doesnt work")
        return None


def get_soup(url) -> BeautifulSoup:
    return BeautifulSoup(make_request(url)[1], 'html.parser')


def get_codes():
    url_name_code = "https://finance.yahoo.com/most-active"
    soup = get_soup(url_name_code)
    codes = {"Code": [], "Name": []}

    code_tds = soup.find_all("td", {"aria-label": "Symbol"})
    for td in code_tds:
        codes["Code"].append(td.text.strip())
    name_tds = soup.find_all("td", {"aria-label": "Name"})
    for td in name_tds:
        codes["Name"].append(td.text.strip())
    return codes


def get_filtered_data_soup(company: str, code: str):
    url_profile = "https://finance.yahoo.com/quote/" + str(company) + "/profile/"

    data = {"Name": [], "Code": [], "Country": [], "Employees": [], "CEO": [], "CEO Year Born": []}
    data["Code"].append(code)
    data["Name"].append(company)

    soup = get_soup(url_profile)
    country_divs = soup.find_all("div", {"class": "address svelte-wxp4ja"})
    if country_divs:
        last_country_div = country_divs[-1]
        data["Country"].append(last_country_div.text.strip())
    dds = soup.find_all("dd")
    for dd in dds:
        strong_tag = dd.find("strong")
        if strong_tag:
            data["Employees"].append(strong_tag.text)

    tables = soup.find_all("table", {"class": "svelte-mj92za"})
    for table in tables:
        tds = table.find_all("td")
        for i, td in enumerate(tds):
            if i % 5 == 0:
                data["CEO"].append(td.text)
            elif (i - 4) % 5 == 0:
                data["CEO Year Born"].append(td.text)

    return data


def get_total_cash_52_range(company: str, code: str):
    url_statistic = "https://finance.yahoo.com/quote/" + str(company) + "/key-statistics/"

    data = {"Name": [], "Code": [], "Total Cash": [], "52-week Change": []}
    data["Code"].append(code)
    data["Name"].append(company)

    soup = get_soup(url_statistic)
    total_cash_tds = soup.find_all("td", {"class": "value svelte-vaowmx"})
    if total_cash_tds:
        total_cash_td = total_cash_tds[14]
        week_change_td = total_cash_tds[24]

        data["Total Cash"].append(total_cash_td.text.strip())
        data["52-week Change"].append(week_change_td.text.strip())

    return data


def get_blackrock(company: str, code: str):
    url_holders = "https://finance.yahoo.com/quote/" + str(code) + "/holders/"
    data = {"Name": [], "Code": [], "Shares": [], "Date Reported": [], "% Out": [], "Value": []}
    data["Code"].append(code)
    data["Name"].append(company)
    soup = get_soup(url_holders)
    table_trs = soup.find_all("tr", {"class": "svelte-1s2g2l0"})

    for tr in table_trs:
        tds = tr.find_all("td")
        if len(tds) >= 5 and tds[0].text.strip().lower() == 'blackrock inc.':
            data["Shares"].append(tds[1].text.strip())
            data["Date Reported"].append(tds[2].text.strip())
            data["% Out"].append(tds[3].text.strip())
            data["Value"].append(tds[4].text.strip())

    return data


'''
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.

'''


def first_task():
    youngest = []
    codes = get_codes()["Code"]
    names = get_codes()["Name"]
    youngest_name = ''
    for i in range(0, len(codes)):
        data = get_filtered_data_soup(codes[i], names[i])
        current_name = names[i]
        current_code = codes[i]

        current_country = data["Country"]
        current_employees = data["Employees"]
        current_CEO_name = data["CEO"]
        current_CEO_year_born = data["CEO Year Born"]
        current_youngest_CEO = 0

        for y in range(1, len(current_CEO_name)):
            if current_CEO_year_born[y] != '-- ' and int(current_CEO_year_born[y]) > current_youngest_CEO:
                youngest_name = str(current_CEO_name[y])
                current_youngest_CEO = int(current_CEO_year_born[y])

        youngest.append(
            [current_youngest_CEO, youngest_name, current_name, current_code, current_country, current_employees])

    result_pretty_table = "==================================== 5 stocks with most youngest CEOs ===================================\n"
    result_pretty_table += "| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |\n"
    result_pretty_table += "===========================================================================================================\n"
    youngest.sort(key=lambda x: x[0])
    for data in reversed(youngest[-5:]):
        result_pretty_table += f"| {data[2]} | {data[3]} | {str(data[4])} | {data[5]} | {data[1]} | {data[0]} |\n"

    print(result_pretty_table)


#first_task()

'''
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
'''


def second_task():
    best_52 = []
    codes = get_codes()["Code"]
    names = get_codes()["Name"]
    best_52_week_change = 0
    for i in range(0, len(codes)):
        data = get_total_cash_52_range(codes[i], names[i])
        if not data["52-week Change"]:
            continue
        current_name = names[i]
        current_code = codes[i]

        current_total_cash = data["Total Cash"]
        current_52_week_change = float(data["52-week Change"][0][:-1])

        if float(current_52_week_change) > best_52_week_change:
            best_52_week_change = current_52_week_change

        best_52.append([current_name, current_code, current_52_week_change, current_total_cash])

    result_pretty_table = "==================================== 10 stocks with best 52-Week Change ===================================\n"
    result_pretty_table += "| Name        | Code | 52-week Change       | Total Cash |\n"
    result_pretty_table += "===========================================================================================================\n"
    best_52.sort(key=lambda x: x[2])
    for data in reversed(best_52[-10:]):
        result_pretty_table += f"| {data[0]} | {data[1]} | {str(data[2])} | {str(data[3])}|\n"

    print(result_pretty_table)


second_task()

'''
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.
'''


def third_task():
    biggest_blackrock = []
    codes = get_codes()["Code"]
    names = get_codes()["Name"]
    for i in range(0, len(codes)):
        data = get_blackrock(names[i], codes[i])
        if not data["Shares"]:
            continue
        current_name = names[i]

        current_code = codes[i]

        current_shares = float(data["Shares"][0][:-1])
        current_date_reported = data["Date Reported"]
        current_perc_out = data["% Out"]
        current_value = data["Value"]

        biggest_blackrock.append(
            [current_name, current_code, current_shares, current_date_reported, current_perc_out, current_value])

    result_pretty_table = "==================================== 10 largest holds of Blackrock Inc ===================================\n"
    result_pretty_table += "| Name        | Code | Shares       | Date Reported | % Out     | Value      |\n"
    result_pretty_table += "===========================================================================================================\n"
    biggest_blackrock.sort(key=lambda x: x[2])
    for data in reversed(biggest_blackrock[-10:]):
        result_pretty_table += f"| {data[0]} | {data[1]} | {str(data[2])} | {data[3]} | {data[4]} | {data[5]} |\n"

    print(result_pretty_table)

#third_task()
