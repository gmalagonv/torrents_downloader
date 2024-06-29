#https://rargb.to/movies/

from playwright.sync_api import sync_playwright
import pandas as pd
import argparse
from dataclasses import dataclass, asdict, field
import os
import sys




@dataclass
class Torrent:
    """holds business data"""

    name: str = None
    resolution: int = None 
    size: float = None
    seeds: int = None



@dataclass
class TorrentList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    torrent_list: list[Torrent] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(torrent) for torrent in self.torrent_list), sep="_"
        )

    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file

        Args:
            filename (str): filename
        """

        # if not os.path.exists(self.save_at):
        #     os.makedirs(self.save_at)
        self.dataframe().to_excel(f"output/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """

        # if not os.path.exists(self.save_at):
        #     os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)



if __name__ == '__main__':
 
    # read search from arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", type=str)
    # parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    
    if args.title:
        search_for = f'{args.title}'
    else:
        search_for = 'Pocahontas'
            
def main():

    with sync_playwright() as p:
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        #checkin_date = '2023-03-23'
        #checkout_date = '2023-03-24'
        fileType = 'movies'
        page_url = f'https://rargb.to/{fileType}/'
        #page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss=Paris&ssne=Paris&ssne_untouched=Paris&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto(page_url, timeout=60000)
        page.wait_for_timeout(5000)
        
        page.locator('//input[@id="searchinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

                    
        # hotels = page.locator('//div[@data-testid="property-card"]').all()
        # print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

            hotels_list.append(hotel_dict)
        
        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False) 
        df.to_csv('hotels_list.csv', index=False) 
        
        browser.close()
            

   