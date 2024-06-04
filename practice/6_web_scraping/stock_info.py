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
from http import cookiejar
from requests.cookies import cookiejar_from_dict, cookielib
from requests.structures import CaseInsensitiveDict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


def make_request(url: str) -> Tuple[int, str]:
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={HEADERS['User-Agent']}")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    try:
        accept_button = driver.find_element(By.CSS_SELECTOR, "button[name='agree']")
        accept_button.click()
        driver.implicitly_wait(5)  
        body = driver.page_source
        s = requests.Session()
        s.cookies.set_policy(BlockAll())
        req = s.get(url, headers=HEADERS)
        status_code = req.status_code
        return (status_code, body)
    except Exception as e:
        print(e)
        return (0, str(e))
    finally:
        driver.quit()

def get_soup(url) -> BeautifulSoup:
    return BeautifulSoup(make_request(url)[1], 'html.parser')

def get_codes():
    url_name_code = "https://finance.yahoo.com/most-active"
    soup = get_soup(url_name_code)
    codes= {"Code": [], "Name": []}
    
    code_tds = soup.find_all("td", {"aria-label": "Symbol"})
    for td in code_tds:
        codes["Code"].append(td.text.strip())
    name_tds = soup.find_all("td", {"aria-label": "Name"})
    for td in name_tds:
        codes["Name"].append(td.text.strip())
    return codes


def get_filtered_data_soup(company: str, code: str):
    url_profile = "https://finance.yahoo.com/quote/"+str(company)+"/profile/"

    
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



'''
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.

'''
def first_task():
    youngest = []
    codes = get_codes()["Code"]
    names = get_codes()["Name"]
    for i in range(0, len(codes)): 
        data = get_filtered_data_soup(codes[i], names[i]) 
        current_name = names[i] 
        current_code = codes[i] 
        current_country = data["Country"]
        current_employees = data["Employees"]
        current_CEO_name = data["CEO"]
        current_CEO_year_born = data["CEO Year Born"]
        current_youngest_index = 0
        current_youngest_CEO = 0

        for y in range(1, len(current_CEO_name)):
            if current_CEO_year_born[y] != '-- ' and int(current_CEO_year_born[y]) >  current_youngest_CEO:
                current_youngest_index = y
                current_youngest_CEO = int(current_CEO_year_born[y])
        
        youngest.append([current_youngest_CEO, current_CEO_name[current_youngest_index], current_name, current_code, current_country, current_employees])

    result_pretty_table = "==================================== 5 stocks with most youngest CEOs ===================================\n"
    result_pretty_table += "| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |\n"
    result_pretty_table += "===========================================================================================================\n"
    youngest.sort(key=lambda x: x[0])
    for data in reversed(youngest[-5:]):
        result_pretty_table += f"| {data[2]} | {data[3]} | {str(data[4])} | {data[5]} | {data[1]} | {data[0]} |\n"

    print(result_pretty_table)

first_task()






