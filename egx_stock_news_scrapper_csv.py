import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime

# Arabic month translation to English
arabic_to_english_months = {
    'يناير': 'January', 'فبراير': 'February', 'مارس': 'March',
    'أبريل': 'April', 'مايو': 'May', 'يونيو': 'June',
    'يوليو': 'July', 'أغسطس': 'August', 'سبتمبر': 'September',
    'أكتوبر': 'October', 'نوفمبر': 'November', 'ديسمبر': 'December'
}

def parse_arabic_date(arabic_date_str):
    # Adjust regex to handle optional year
    date_parts = re.search(r'(\d{1,2})\s(\w+)\s((\d{4})\s)?(\d{1,2}):(\d{2})\s(ص|م)', arabic_date_str)
    if not date_parts:
        return None

    day, month_arabic, _, year, hour, minute, period = date_parts.groups()
    
    # If year is missing in the date string, use the current year
    if year is None:
        year = datetime.now().year

    # Convert Arabic '00' hour in PM to '12' to comply with 12-hour clock rules
    if period == 'م' and hour == '00':
        hour = '12'

    month_english = arabic_to_english_months.get(month_arabic, 'January')  # Default to January if month is not found
    date_string = f"{day} {month_english} {year} {hour}:{minute} {'AM' if period == 'ص' else 'PM'}"
    
    # Parse the date string into a datetime object
    parsed_date = datetime.strptime(date_string, '%d %B %Y %I:%M %p')
    return parsed_date.strftime('%Y-%m-%d %H:%M')



def scrape_stock_news(stock_symbol):
    base_url = 'https://www.mubasher.info/markets/EGX/stocks'
    stock_url = f"{base_url}/{stock_symbol}/news"
    
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_container = soup.find_all('div', class_='mi-article-media-block md-whiteframe-z1')
    
    news_list = []
    
    for news in news_container:
        title = news.find('a', class_='mi-article-media-block__title').get_text(strip=True)
        link = news.find('a', class_='mi-article-media-block__title')['href']
        arabic_date = news.find('span', class_='mi-article-media-block__date').get_text(strip=True)
        date = parse_arabic_date(arabic_date)  # Convert Arabic date to standard format
        summary = news.find('div', class_='mi-article-media-block__text').get_text(strip=True) if news.find('div', class_='mi-article-media-block__text') else 'No summary available'
        
        news_list.append([title, date, summary, link])
    
    return news_list

def save_news_to_csv(news_data, filename='news.csv'):
    fieldnames = ['title', 'date', 'summary', 'link']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(news_data)

stock_symbol = 'ISMQ'
news = scrape_stock_news(stock_symbol)
save_news_to_csv(news)