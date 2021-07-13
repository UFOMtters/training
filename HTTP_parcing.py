import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

URL = 'https://www.kommersant.ru/search/results'

### Main function
### https://github.com/UFOMtters/training.git
def get_all_links(URL, quary, pages):
    all_refs = []
    param = {'search_query': quary}
    for i in range(1, pages+1):
        param['page'] = i
        res = requests.get(URL, param)
        soup = BeautifulSoup(res.text, 'html.parser')
        new_blocks = soup.find_all('div', class_='search_results_item')
        articles_intro = list(map(lambda x: x.find('div', class_='article_intro'), new_blocks))
        a_list = list(map(lambda x: x.find('a').get('href'), articles_intro))
        all_refs += list(map(lambda x: 'https://www.kommersant.ru' + x, a_list))
    return all_refs

all_limks = get_all_links(URL, 'python', 3)
kon_news = pd.DataFrame()
for link in all_limks:
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    time.sleep(0.3)
    if soup.find('div', class_='b-article__publish_date'):
        date = pd.to_datetime(soup.find('div', class_='b-article__publish_date').find('time').get('datetime'), dayfirst=True).date()
    elif soup.find('time', class_='title__cake'):
        date = pd.to_datetime(soup.find('div', class_='title__cake').find('time').get('datetime'), dayfirst=True).date()
    if soup.find('h2', class_='article_name'):
        title = soup.find('h2', class_='article_name').text
    else:
        title = soup.find('h1', class_='article_name').text
    text = soup.find('div', class_= 'article_text_wrapper').text
    row = {'date': date, 'title': title, 'text': text}
    kon_news = pd.concat([kon_news, pd.DataFrame([row])])
print(kon_news)