from bs4 import BeautifulSoup
import requests
from news.news_info import NewsInfo
from scraper.scraper import Scraper


class ManilaTimesScraper(Scraper):
    BASE_URL = 'https://www.manilatimes.net/tag/climate-change/page/{}'
    ARTICLE_SET = set()
    
    def scrape(self):
        for i in range(9):
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
                
                news_info = self.extract_news_info(response)
                
                if (news_info is None):
                    continue

                self.df.add_news('Manila Times', news_info)

    def get_results(self, response: requests.Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('div', class_='tag-widget').find('div', class_='item-row-2').find_all('a', href=True)
    
    def extract_news_info(self, response: requests.Response):
        try: 
            soup = BeautifulSoup(response.text, 'html.parser')
            article_title = soup.find('h1', class_='article-title').text

            article_byline = soup.find('a', class_='article-author-name').text

            article_published = soup.find('div', class_='article-publish-time').text

            article_content = [paragraph.text for paragraph in soup.find('div', 'article-body-content').find_all('p')]

            article_section = response.url.split('/')[6]
            return NewsInfo(
                article_published, 
                article_title,
                article_byline,
                article_section,
                article_content
            )
        
        except Exception as e:
            with open('./log/{}.txt'.format('err'), 'a') as file:
                file.write(str(e))

            return None
        
