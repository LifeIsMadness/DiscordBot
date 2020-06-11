import re
import requests
from bs4 import BeautifulSoup





class IgromaniaNewsParser(object):
#    news_url = 'https://www.igromania.ru/news/'
#    html_text = requests.get(news_url).text
#    soup = BeautifulSoup(html_text, 'html.parser')
    
    
    def __init__(self, last_news_file):
        self._last_news_file = last_news_file
        self._read_last_key()
        self._site_url = 'https://www.igromania.ru/'
    
    
    
    def _read_last_key(self):
        with open(self._last_news_file, 'r') as desc:
            self._last_news_key = desc.read()
    
    
    def _store_last_key(self, last_news_key):
        with open(self._last_news_file, 'w') as desc:
            desc.write(last_news_key)      
    
    
    def _create_soup(self):
        html_text = requests.get(self._site_url + 'news/').text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup
    
    
    def _news_updated(self):
        soup = self._create_soup()
        attrs = {
            'class': 'aubl_item',
	        
        }
        
        news_element =  soup.find('div', attrs=attrs)
        return news_element.a.img.get('src') + '\n' != self._last_news_key
              
    
    def parse_news(self):
        if not self._news_updated():
            return
        soup = self._create_soup()
        attrs = {
            'class': 'aubl_item',
	        
        }
        
        news_elements =  soup.find_all('div', attrs=attrs, limit=3)
        self._store_last_key(news_elements[0].a.img.get('alt'))
        news_elements.reverse()
        return news_elements
#        for element in news_elements:
#            print(element.a.img.get('alt'))


if __name__ == '__main__':
    news_parser = IgromaniaNewsParser('key.txt')
    news_parser.parse_news()

