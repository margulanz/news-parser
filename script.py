import requests
import time
import csv
from bs4 import BeautifulSoup
from datetime import datetime

# URL of the website


# Function to check if news is already recorded
def is_news_recorded(news_title):
    with open('recorded_news.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Title'] == news_title:
                return True
    return False

# Function to record news


def record_news(news_author, news_title, news_text):
    with open('recorded_news.csv', 'a', newline='') as file:
        fieldnames = ['Author', 'Title', 'Text', 'Time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header if file is empty
        # file.seek(0)
        # first_char = file.read(1)
        # if not first_char:
        #     writer.writeheader()

        writer.writerow({'Author': news_author, 'Title': news_title,
                        'Text': news_text, 'Time': datetime.now()})


def update_news():
    url = 'https://finance.yahoo.com/topic/stock-market-news/'
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        fin_stream = soup.find('div', id='Fin-Stream')

        # Find all news items
        news = fin_stream.find_all('li', class_='js-stream-content Pos(r)')
        for new in news:
            news_data = new.get_text("~").split("~")
            author = news_data[0]
            title = news_data[1]
            text = news_data[2]
            # print("New news found:", news_text)
            if not is_news_recorded(title):
                print("New news found:", title)
                record_news(author, title, text)
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
