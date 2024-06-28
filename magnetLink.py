import requests
from bs4 import BeautifulSoup
import sys

def get_magnet_link(url):

    print(type(url), url)

        


    # Make a request to the website
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first anchor tag with an href containing "magnet:"
        magnet_link_tag = soup.find('a', href=lambda x: x and 'magnet:' in x)

        # Extract the magnet link
        if magnet_link_tag:
            magnet_link = magnet_link_tag.get('href')
            return magnet_link

    # Return None if the request fails or if the magnet link is not found
    return None

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def read_from_file():
    try:
        file_path = '/home/gerard/nextcloud/bash_stuff/scripts/downloading_movies/url.txt'
        with open(file_path, "r") as file:
            url = file.readline().strip()
            url_start_index = url.find('https://')

            # Extract the URL part
            url = url[url_start_index:]
        
    except FileNotFoundError:
        url = 0
        print(f"Error: File not found - {file_path}")

    except Exception as e:
        url = 0
        print(f"Error: {e}")

    return url




if __name__ == "__main__":
    # Check if a URL is provided as a command-line argument
    # print(len(sys.argv) )
    if len(sys.argv) < 2:
        print("Usage: python script.py <url>")
        sys.exit(1)
    try:
        if int(sys.argv[1]) == 0:
            url = read_from_file()

    except:
        url = sys.argv[1]

    # Get the URL from the command-line argument
    if url == 0:
        sys.exit(1)


    # Call the function
    magnet_link = get_magnet_link(url)

    # Print the result
    if magnet_link:
        print(f'Magnet Link: {magnet_link}')

        # Save the magnet link to a file named 'magnet_link.txt'
        magnet_link = '"' + magnet_link + '"'
        save_to_file('/home/gerard/nextcloud/bash_stuff/scripts/downloading_movies/magnet_link.txt', magnet_link)

        print('Magnet link saved to magnet_link.txt')
    else:
        print('Magnet link not found.')
