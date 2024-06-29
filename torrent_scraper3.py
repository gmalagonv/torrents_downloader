import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


############################################################################

def extract_page_number(url):
    pattern = r'/search/(\d+)/\?search='
    match = re.search(pattern, url)
    if match:
        return int(match.group(1))



def main(title = 'the godfather', category = 'movies'):
    r = 0
    url_torrent = 'https://rargb.to/'
    url_head = 'https://rargb.to/search'
    url_tail = f'/?search={title}&category[]={category}'
    torrents_data = pd.DataFrame(columns=["title", "link", "size", "seeds"])
#    url = f'https://rargb.to/search/?search={title}&category[]={category}'
    url = url_head + url_tail
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pager_links = soup.find(id ='pager_links')
    if pager_links is None:
        last_link_num = 1
    else:
        links = pager_links.find_all('a', href=True)
        last_link = (links[-1])
        last_link_num = extract_page_number(last_link['href'])

    for page in range(1,last_link_num+1):
        url_page = url_head + '/' + str(page) + url_tail
        response_p = requests.get(url_page)
        soup_p = BeautifulSoup(response_p.content, 'html.parser')
        #table = soup_p.find('table', class_ = 'lista2t').find_all('tr', class_ = 'lista2')
        table = soup_p.find_all('tr', class_ = 'lista2')

        
        print('page**************', page,'\n', url_page, '\n')#)

        if len(table) == 0:
            print(soup_p)


        #print(table)
        for row in table:
            r += 1
            #print('torrent ',r)
            col = row.find_all("td")
            a_tag = (col[1].find('a'))
            title = a_tag.text.strip()
            link = url_torrent + a_tag.get('href')
            size = float((col[4].text).split()[0])
            seeds = int(col[5].text)
            torrents_data = pd.concat([torrents_data, pd.DataFrame({"title": [title], "link": [link], "size": [size], "seeds": [seeds]})], ignore_index=True)
            #torrents_data = torrents_data.append({"title":title, "link":link, "size":size, "seeds":seeds}, ignore_index=True)
            #print(col[1].find('a', title=True), '\n',col[1].find('a', href=True)['href'])
    print(torrents_data)
            



if __name__ == '__main__':
    main()