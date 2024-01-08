from news.news_df import NewsDataFrame
from news.news_info import NewsInfo
from scraper.scraper import Scraper

import requests
from bs4 import BeautifulSoup, ResultSet

class InquirerScraper(Scraper):
    BASE_URL = 'https://{}.inquirer.net/tag/climate-change/page/{}'
    SECTIONS = [
        'newsinfo',
        'globalnation',
        'business',
        'lifestyle',
        'entertainment',
        'technology',
        'sports',
        'opinion'
    ]

    def get_results_from_search(self, url: str, section) -> ResultSet[any]:
        
        results_html = requests.get(url, headers=self.HEADERS)
        
        if results_html.url == 'https://{}.inquirer.net'.format(section):
            return None

        soup = BeautifulSoup(results_html.text, 'html.parser')
        
        return soup.find_all('div', id='ch-ls-head')
    
    def get_result_page(self, result):
        result_url = result.find('a', href=True).get('href')
        return requests.get(result_url, headers=self.HEADERS)
    
    def extract_news_info(self, result: requests.Response, section) -> NewsInfo:
        page = BeautifulSoup(result.text, 'html.parser')

        article_name = page.find('h1', class_='entry-title').text
        
        if (page.find('div', id='art_author') is None):
            try:
                article_author = page.find('div', id='art_plat').find('a').text
            except Exception as e:
                print(e)
                return None

        else:
            article_author = page.find('div', id='art_author')\
                .find('span').find('a').text
            
        article_plat = page.find('div', id='art_plat').text.split('/')
        article_published = article_plat[len(article_plat) - 1].strip()

        article_content = [p.text for p in page.find('div', id='article_content').find_all('p') ]

        article_section = section

        return NewsInfo(
            article_published, 
            article_name, 
            article_author, 
            article_section, 
            article_content)

    def scrape(self) -> list[NewsInfo]:
        for section in self.SECTIONS:
            for i in range(80):
                url = self.BASE_URL.format(section, i + 1)
                results = self.get_results_from_search(url, section)

                if results is None:
                    break

                print('Fetching from URL {}'.format(url))
                
                for i, result in enumerate(results):
                    result_page = self.get_result_page(result)                    
                    print(f'\tScraping data from { result_page.url }')

                    news_info = self.extract_news_info(result_page, section)
                    self.articles.append(news_info)

                    if (news_info is None):
                        with open('./log/{}.txt'.format('err'), 'a') as file:
                            file.write(result.text)
                        continue

                    self.df.add_news('Inquirer', news_info)
                
