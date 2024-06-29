import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

def extract_page_number(url):
    pattern = r'/search/(\d+)/\?search='
    match = re.search(pattern, url)
    if match:
        return int(match.group(1))

def selenium_scraper(url):
    # Set up Selenium WebDriver for Chrome
    options = ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome_driver_path = '/usr/local/bin/chromedriver'  # Update to the path where you have chromedriver

    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the target URL
    driver.get(url)

    # Wait for the page to load and display the table
    driver.implicitly_wait(2)

    # Get the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the table rows
    table_rows = soup.find_all('tr', class_='lista2')

    # Print the number of rows found
    print(f'Number of table rows with class "lista2": {len(table_rows)}')

    # Close the WebDriver
    driver.quit()
    
    return table_rows


def fromRows2df(table_rows, df_data):

    url_torrent = 'https://rargb.to/'

    for row in table_rows:
        col = row.find_all("td")
        a_tag = (col[1].find('a'))
        title = a_tag.text.strip()
        link = url_torrent + a_tag.get('href')
        size = float((col[4].text).split()[0])
        seeders = int(col[5].text)
        leechers = int(col[5].text)

         # do not add if seeders = 0
        if seeders != 0:
            df_data = pd.concat([df_data, pd.DataFrame({"title": [title], "link": [link], 
                                                                "size": [size], "seeders": [seeders],
                                                                "leechers" : [leechers]})], ignore_index=True)
    return df_data

def rate_torrent(df_data):

    # Score = a×Seeders − b×Leechers− c×Size
    
    a = 2
    b = 1
    c = 0.1
    
    # df_data['seeders'] = df_data['seeders'] * a
    # df_data['leechers'] = df_data['leechers'] * b
    # df_data['size'] = df_data['size'] * c

    df_data['score'] = df_data['seeders'] * a + df_data['leechers'] * b + df_data['size'] *c
    df_data = df_data.sort_values(by='score',ascending=False)
    df_data = df_data.reset_index(drop=True)

    return df_data



def main(title='godfather', category='movies'):
    r = 0
    url_head = 'https://rargb.to/search'
    url_tail = f'/?search={title}&category[]={category}'
    
    df_data = pd.DataFrame(columns=["title", "link", "size", "seeders", "leechers"])


    url = url_head + url_tail
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pager_links = soup.find(id='pager_links')
    if pager_links is None:
        last_link_num = 1
    else:
        links = pager_links.find_all('a', href=True)
        last_link = links[-1]
        last_link_num = extract_page_number(last_link['href'])

    # Looping over each page
    for page in range(1, last_link_num + 1):
        url_page = url_head + '/' + str(page) + url_tail
        print('page**************', page, '\n', url_page, '\n')

        table_rows = selenium_scraper(url_page)
        df_data = fromRows2df(table_rows, df_data)

    df_data = rate_torrent(df_data)
    print(df_data)

if __name__ == '__main__':
    main()
