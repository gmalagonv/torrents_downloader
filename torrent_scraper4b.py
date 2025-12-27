import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

import argparse
import subprocess
import platform


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

    # Close the WebDriver

    driver.quit()
    
    return soup

def selenium_scraper_raspberry(url):
    # Set up Selenium WebDriver for Chrome
    options = ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/chromium'  # Specify chromium on Raspberry Pi
    
    # For Raspberry Pi, let Selenium find chromedriver automatically
    # Remove the executable_path parameter
    driver = webdriver.Chrome(options=options)

    # Navigate to the target URL
    driver.get(url)

    # Wait for the page to load and display the table
    driver.implicitly_wait(2)

    # Get the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the WebDriver
    driver.quit()
    
    return soup

def selenium_scraper_raspberry2(url):
    # Set up Selenium WebDriver for Chrome
    options = ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # For Raspberry Pi, specify chromium binary location
    options.binary_location = '/usr/bin/chromium'
    
    # REMOVE THESE LINES:
    # chrome_driver_path = '/usr/local/bin/chromedriver'  # Delete this line
    # service = ChromeService(executable_path=chrome_driver_path)  # Delete this line
    
    # REPLACE WITH:
    # Let Selenium find chromedriver automatically
    driver = webdriver.Chrome(options=options)

    # Navigate to the target URL
    driver.get(url)

    # Wait for the page to load and display the table
    driver.implicitly_wait(2)

    # Get the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the WebDriver
    driver.quit()
    
    return soup



def fromRows2df(table_rows, df_data):

    url_torrent = 'https://rargb.to/'

    for row in table_rows:
        col = row.find_all("td")
        a_tag = (col[1].find('a'))
        title = a_tag.text.strip()
        link = url_torrent + a_tag.get('href')

        if '1080p' in title:
            res = 1080
        elif '720p' in title:
            res = 720
        else:
            res = None

        size = float((col[4].text).split()[0])
        seeders = int(col[5].text)
        leechers = int(col[5].text)

         # do not add if seeders = 0
        if seeders != 0 and size <= 10:
            df_data = pd.concat([df_data, pd.DataFrame({"title": [title], "link": [link], "resolution": [res],
                                                                "size(GB)": [size], "seeders": [seeders],
                                                                "leechers" : [leechers]})], ignore_index=True)
    return df_data

def rate_torrent(df_data):

    # Score = a×Seeders − b×Leechers− c×Size
    
    a = 2
    b = 1
    c = 0.1
    

    df_data['score'] = df_data['seeders'] * a + df_data['leechers'] * b + df_data['size(GB)'] *c
    df_data = df_data.sort_values(by='score',ascending=False)
    df_data = df_data.reset_index(drop=True)
    
    # keep a max of 15 results
    df_data = df_data.head(15)
    
    return df_data



def df_torrents(title='godfather', category='movies', save2csv = False):

    url_head = 'https://rargb.to/search'
    url_tail = f'/?search={title}&category[]={category}'
    
    df_data = pd.DataFrame(columns=["title", "link", "resolution", "size(GB)", "seeders", "leechers"])


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
        
        if platform.machine() == "armv7l":
            soup2 = selenium_scraper_raspberry2(url_page)
        else:
            soup2 = selenium_scraper(url_page)

        # Extract the table rows
        table_rows = soup2.find_all('tr', class_='lista2')

        # Print the number of rows found
        print(f'Number of table rows with class "lista2": {len(table_rows)}')
            
        
        df_data = fromRows2df(table_rows, df_data)

    df_data = rate_torrent(df_data)
    
    if save2csv:
        df_data.to_csv(title + '_torrent_list.csv')

    
    return df_data




def selector(df_data, autoSelector=False):
    
    confirmation_input = "n"
    
    if autoSelector == False:
        while confirmation_input == "n":

            print(df_data[["title","resolution", "size(GB)", "seeders", "leechers", "score"]])

            # Prompt the user to enter a list of values
            user_input = input("\n*********************** \nWhich one(s) do you want to download?\nEnter a list of indexes separated by commas:")
                    # Convert the input string into a list of strings
            user_list = user_input.split(',')

            # Convert the list of strings to a list of integers
            user_list = [int(item.strip()) for item in user_list]

            # Print the resulting list
            print("\nThe list of selected movies:\n", df_data.loc[user_list, ["title","resolution", "size(GB)", "seeders", "leechers", "score"]])
            confirmation_input = input("\n do you confirm yout choice? (y/n): ")

            if confirmation_input == "y":
                df_data = df_data.loc[user_list, 'link']
    else:
        df_data = df_data.loc[0, 'link']
    
    
    return df_data




def downloader(df_data):

    for i in range(0,df_data.size):

        url = df_data.iloc[i]

        if platform.machine() == "armv7l":
            soup = selenium_scraper_raspberry2(url)
        else:
            soup = selenium_scraper(url)

        soup = selenium_scraper(url)
        magnet_link_tag = soup.find('a', href=lambda x: x and 'magnet:' in x)

        # Extract the magnet link
        print(magnet_link_tag)
        if magnet_link_tag:
            magnet_link = magnet_link_tag.get('href')
            print(f"Adding to Transmission: {magnet_link}")
            
            # Send to transmission-daemon
            try:
                subprocess.run([
                    'transmission-remote', 
                    'localhost:9091',  # Transmission RPC address
                    '-a', 
                    magnet_link
                ], check=True)
                print("✅ Torrent added successfully!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to add torrent: {e}")





if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", type=str)
    parser.add_argument("-s", "--save", type=bool)
    # parser.add_argument("-a", "--auto", type=bool)

    args = parser.parse_args()
    

    df_data = df_torrents(args.title, 'movies', args.save)
    df_data = selector(df_data)
    downloader(df_data)

