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


from typing import Tuple
import urllib.request
import ssl
import gzip
from io import BytesIO
from bs4 import BeautifulSoup
from pprint import pprint  
import requests

ssl._create_default_https_context = ssl._create_stdlib_context

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


def make_request(url: str) -> Tuple[int, str]:
    req = urllib.request.Request(url, headers=HEADERS)
    #req_without_cookies = urllib.request.Request(url=url, headers=HEADERS,cook)
    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.getcode()
            # Check if the response is gzip-compressed
            if resp.info().get('Content-Encoding') == 'gzip':
                buf = BytesIO(resp.read())
                f = gzip.GzipFile(fileobj=buf)
                body = f.read().decode('utf-8')
            else:
                body = resp.read().decode('utf-8')
            return (status_code, body)
    except Exception as e:
        print(e)
        return (0, str(e))

def get_soup(url) -> BeautifulSoup:
    return BeautifulSoup(make_request(url)[1], 'html.parser')

def get_filtered_data_soup(company: str):
    url_name_code = "https://finance.yahoo.com/most-active"
    url_profile = "https://finance.yahoo.com/quote"+str(company)+"/profile/"

    soup = get_soup(url_name_code)
    data = {"Name": [], "Code": [], "Country": [], "Employees": [], "CEO": [], "CEO Year Born": []}
    name_tds = soup.find_all("td", {"aria-label": "Name"})
    for td in name_tds:
        print("name:" + td.text.strip())
        data["Name"].append(td.text.strip())
    code_tds = soup.find_all("td", {"aria-label": "Symbol"})
    for td in code_tds:
        data["Code"].append(td.text.strip())
    soup = get_soup(url_profile)
    country_divs = soup.find_all("div", {"class": "address svelte-wxp4ja"})
    if country_divs:
        last_country_div = country_divs[-1]
        data["Country"].append(last_country_div.text.strip())
    dds = soup.find_all("dd") #Sa 2 dd w soup i w jednym jest strong wiec nie bedzie duzo szukania
    for dd in dds:
        strong_tag = dd.find("strong")
        if strong_tag:
            print(strong_tag.text)
            data["Employees"].append(strong_tag.text)
    
    tables = soup.find_all("table", {"class": "svelte-mj92za"}) #Sa 2 dd w soup i w jednym jest strong wiec nie bedzie duzo szukania
    for table in tables:
        tds = table.find_all("td")
        for i, td in enumerate(tds):
            if i % 5 == 0:
                data["CEO"].append(td.text)
            elif (i - 4) % 5 == 0:
                data["CEO Year Born"].append(td.text)
    
    pprint(data)




   

   



def first_task():
    ...

print(get_soup("https://finance.yahoo.com/quote/AAL/profile"))

#get_filtered_data_soup("AAL")