#https://rargb.to/search/?search=pocahontas&category[]=movies


from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    
    with sync_playwright() as p:
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        title = 'Pocahontas'
        category = 'movies'
        
        page_url = f'https://rargb.to/search/?search={title}&category[]={category}'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
                    
        results = page.locator('.lista').all()
        print(results)
        # print(f'There are: {len(hotels)} hotels.')

        # hotels_list = []
        # for hotel in hotels:
        #     hotel_dict = {}
        #     hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
        #     hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
        #     hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
        #     hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
        #     hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

        #     hotels_list.append(hotel_dict)
        
        # df = pd.DataFrame(hotels_list)
        # df.to_excel('hotels_list.xlsx', index=False) 
        # df.to_csv('hotels_list.csv', index=False) 
        
        browser.close()
            
if __name__ == '__main__':
    main()