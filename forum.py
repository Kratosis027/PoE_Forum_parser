import requests
from bs4 import BeautifulSoup
import csv


HOST = 'https://www.pathofexile.com/'
URL = 'https://www.pathofexile.com/forum/view-forum/news/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}
FILE = 'news.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_number_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_="botBar last forumControls").find_all('a')
    if pagination:
        return pagination[-2].get_text()
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='')
    items_even = soup.find_all('tr', class_='even')
    news = []
    for item in items:
        news.append(
            {
                'title': item.find('div', class_='title').get_text(strip=True),
                'post_by': item.find('div', class_='postBy').find('a').get_text(strip=True),
                'date': item.find('div', class_='postBy').find('span', class_='post_date').get_text(strip=True).replace
                (',', ' '),
            }
        )
    for item in items_even:
        news.append(
            {
                'title': item.find('div', class_='title').get_text(strip=True),
                'post_by': item.find('div', class_='postBy').find('a').get_text(strip=True),
                'date': item.find('div', class_='postBy').find('span', class_='post_date').get_text(strip=True).replace
                (',', ' '),
            }
        )
    return news


def save_file(items, path):
    with open(path, 'w', newline='',) as file:
        writer = csv.writer(file)
        writer.writerow(['Theme', 'Author', 'Data'])
        for position in items:
            writer.writerow([position['title'], position['post_by'], position['date']])


def parser():
    request_parse = int(input("Число страниц спарсить: "))
    html = get_html(URL)
    if html.status_code == 200:
        news = []
        get_number_pages(html.text)
        for page in range(1, request_parse+1):
            print(f'Парсин страницы: {page} из {request_parse}')
            html = get_html(URL, params={'page': page})
            news.extend(get_content(html.text))
        save_file(news, FILE)
    else:
        print("Не получилось что то")


parser()
