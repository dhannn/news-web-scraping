from bs4 import BeautifulSoup
import requests
from scraper.scraper import Scraper


class ManilaTimesScraper(Scraper):
    BASE_URL = 'https://www.manilatimes.net/tag/climate-change/page/{}'
    ARTICLE_SET = set()
    
    def scrape(self):
        for i in range(1):
            url = self.BASE_URL.format(i + 1)
            response = requests.get(url, headers=self.HEADERS)
            print(f'Fetching results from {url}')

            result_urls = map(lambda x: x['href'], self.get_results(response))
            for result_url in result_urls:
                if result_url in self.ARTICLE_SET:
                    continue

                self.ARTICLE_SET.add(result_url)
                print(f'\tScraping data from {result_url}')
                response = requests.get(result_url, headers=self.HEADERS)
                self.extract_news_info(response)

    def get_results(self, response: requests.Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('div', class_='tag-widget').find('div', class_='item-row-2').find_all('a', href=True)
    
    def extract_news_info(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        article_title = soup.find('h1', class_='article-title').text
        print(article_title)

        article_byline = soup.find('a', class_='article-author-name').text
        print(article_byline.split(' ', 1)[1])

        article_published = soup.find('div', class_='article-publish-time').text
        print(article_published)

        article_content = map(lambda x: x.text, soup.find('div', 'article-body-content').find_all('p'))
        print('\n'.join(article_content))
