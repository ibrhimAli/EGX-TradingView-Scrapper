import requests
from bs4 import BeautifulSoup

def get_historical_data_url(stock_symbol):
    # Construct the URL dynamically with the given stock symbol
    url = f'https://www.mubasher.info/markets/EGX/stocks/{stock_symbol}'
    
    # Send HTTP GET request to the website
    response = requests.get(url)
    if response.status_code != 200:
        return 'Failed to retrieve data from the website'
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Navigate through the HTML structure
    mi_content = soup.find('div', class_="mi-content")
    if not mi_content:
        return 'mi-content division not found.'

    mi_main_content = mi_content.find('main', class_="mi-main-content")
    if not mi_main_content:
        return 'mi-main-content division not found.'

    # Find the div that contains the 'historical-data-url'
    historical_data_container = mi_main_content.find('div', attrs={"historical-data-url": True})
    if historical_data_container:
        return historical_data_container['historical-data-url']
    else:
        return 'Historical data URL not found.'

# Example usage:
stock_symbol = 'ISMQ'  # This can be dynamically changed as needed
historical_data_url = get_historical_data_url(stock_symbol)
print(historical_data_url)