import re
import requests
from bs4 import BeautifulSoup


class IgromaniaNewsParser(object):
    def __init__(self, last_news_file, news_per_request=3):
        self._limit = news_per_request
        self._last_news_file = last_news_file
        self.site_url = 'https://www.igromania.ru/'


    def _read_last_key(self):
        with open(self._last_news_file, 'r') as desc:
            return desc.read().strip()

    def _store_last_key(self, last_news_key):
        with open(self._last_news_file, 'w') as desc:
            desc.write(last_news_key)

    def _create_soup_with_attrs(self):
        html_text = requests.get(self.site_url + 'news/').text
        soup = BeautifulSoup(html_text, 'html.parser')
        attrs = {
            'class': 'aubl_item',
        }
        return soup, attrs

    def _news_updated(self, last_news_key):
        soup, attrs = self._create_soup_with_attrs()
        news_element = soup.find('div', attrs=attrs)
        return news_element.a.img.get('src') != last_news_key


    def parse_news(self):
        self._last_news_key = self._read_last_key()
        if not self._news_updated(self._last_news_key):
            return []

        soup, attrs = self._create_soup_with_attrs()
        news_elements = soup.find_all('div', attrs=attrs, limit=self._limit)
        news_elements = self._remove_viewed_news(news_elements, self._limit)
        self._store_last_key(news_elements[-1].a.img.get('src'))
        return news_elements


    def _remove_viewed_news(self, news_elements, limit):
        for i in range(1, limit):
            if news_elements[i].a.img.get('src') + '\n' == self._last_news_key:
                news_elements = news_elements[:i]
                break
        news_elements.reverse()
        return news_elements


if __name__ == '__main__':
    news_parser = IgromaniaNewsParser('key.txt')
    news_parser.parse_news()
