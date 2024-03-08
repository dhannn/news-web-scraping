from telnetlib import EC
from bs4 import BeautifulSoup
from news.news_info import NewsInfo
from scraper.scraper import Scraper
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class ManilaTimesScraper(Scraper):
    BASE_URL = 'https://www.manilatimes.net/tag/{}/page/{}'
    ARTICLE_SET = set()
    
    def scrape(self):
        login_url = 'https://www.manilatimes.net/premium'
        driver = webdriver.Chrome()
        driver.get(login_url)

        signin = driver.find_element(By.ID, "signInButton")
        WebDriverWait(driver, timeout=100, poll_frequency=1).until(EC.staleness_of(signin))

        driver.implicitly_wait(1)

        page_num = {'climate-change': 9, 'global-warming': 2}
        for keyword in self.keywords:

            for i in range(page_num[keyword]):
                url = self.BASE_URL.format(keyword, i + 1)
                driver.get(url)

                print(f'Fetching results from {url}')

                result_urls = map(lambda x: x['href'], self.get_results(driver.page_source))
                for result_url in result_urls:
                    if result_url in self.ARTICLE_SET:
                        continue

                    self.ARTICLE_SET.add(result_url)
                    print(f'\tScraping data from {result_url}')
                    
                    driver.get(result_url)
                    news_info = self.extract_news_info(driver.page_source, result_url, keyword)
                    
                    if (news_info is None):
                        continue

                    self.df.add_news('Manila Times', news_info)

    def get_results(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        return soup.find('div', class_='tag-widget').find('div', class_='item-row-2').find_all('a', href=True)
    
    def extract_news_info(self, response, url, keyword):
        try: 
            soup = BeautifulSoup(response, 'html.parser')
            article_title = soup.find('h1', class_='article-title').text.strip()

            article_byline = soup.find('a', class_='article-author-name').text.strip() if soup.find('a', class_='article-author-name') is not None else None

            article_published = soup.find('div', class_='article-publish-time').text.strip() if soup.find('div', class_='article-publish-time') is not None else None

            article_content = [paragraph.text.strip() for paragraph in soup.find('div', 'article-body-content').find_all('p')]

            article_section = url.split('/')[6].strip()
            return NewsInfo(
                keyword,
                article_published, 
                article_title,
                article_byline,
                article_section,
                article_content
            )
        
        except Exception as e:
            print("ERROR: " + str(e))

            with open('./log/{}.txt'.format('err'), 'a') as file:
                file.write('[' + url + ']' + str(e) + '\n')

            return None
        
