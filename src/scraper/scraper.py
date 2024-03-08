from news.news_df import NewsDataFrame
from news.news_info import NewsInfo

class Scraper:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    keywords = None

    articles = []
    
    def __init__(self, df: NewsDataFrame, keywords):
        self.df = df
        self.keywords = keywords

    def scrape(self) -> list[NewsInfo]:
        pass
