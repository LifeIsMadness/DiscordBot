import re
import requests
from bs4 import BeautifulSoup


class IgromaniaNewsParser(object):
    def __init__(self, last_news_file):
        self._last_news_file = last_news_file
        self.site_url = 'https://www.igromania.ru/'

    def _read_last_key(self):
        with open(self._last_news_file, 'r') as desc:
            return desc.read().strip()

    def _store_last_key(self, last_news_key):
        with open(self._last_news_file, 'w') as desc:
            desc.write(last_news_key)

    def _create_soup(self):
        html_text = requests.get(self.site_url + 'news/').text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup

    def _news_updated(self, last_news_key):
        soup = self._create_soup()
        attrs = {
            'class': 'aubl_item',

        }

        news_element = soup.find('div', attrs=attrs)
        return news_element.a.img.get('src') != last_news_key

    def parse_news(self):
        last_news_key = self._read_last_key()
        if not self._news_updated(last_news_key):
            return []
        soup = self._create_soup()
        attrs = {
            'class': 'aubl_item',

        }

        news_elements = soup.find_all('div', attrs=attrs, limit=3)
        for i in range(1, 3):
            if news_elements[i].a.img.get('src') + '\n' == last_news_key:
                news_elements = news_elements[:i]
                break
        self._store_last_key(news_elements[0].a.img.get('src'))
        news_elements.reverse()
        return news_elements
#        for element in news_elements:
#            print(element.a.img.get('alt'))


if __name__ == '__main__':
    news_parser = IgromaniaNewsParser('key.txt')
    news_parser.parse_news()
