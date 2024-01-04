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
        'enterntainment',
        'technology',
        'sports',
        'opinion'
    ]
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    articles = []

    def get_results_from_search(self, url: str) -> ResultSet[any]:
        
        results_html = requests.get(url, headers=self.HEADERS).text
        soup = BeautifulSoup(results_html, 'html.parser')
        
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

        article_content = page.find('div', id='article_content').getText()

        article_section = section

        return NewsInfo(
            article_published, 
            article_name, 
            article_author, 
            article_section, 
            article_content)

    def scrape(self) -> list[NewsInfo]:
        for section in self.SECTIONS:
            for i in range(100):
                url = self.BASE_URL.format(section, i)
                results = self.get_results_from_search(url)

                print('Fetching from URL {}'.format(url))
                
                for result in results:
                    result_page = self.get_result_page(result)                    
                    news_info = self.extract_news_info(result_page, section)
                    self.articles.append(news_info)

                    if (news_info is None):
                        with open('../log/err_{}.txt'.format(result))as file:
                            file.write(result)

                    print(news_info.headline)
                    print(news_info.byline, '\n\n')

                
