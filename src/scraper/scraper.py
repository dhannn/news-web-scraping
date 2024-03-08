from news.news_df import NewsDataFrame
from news.news_info import NewsInfo

class Scraper:    
    """
    Base class for web scrapers that extract news information.

    Attributes:
        HEADERS (dict): Default headers to be used in web requests.

    Methods:
        __init__(self, df: NewsDataFrame, keywords):
            Initializes a Scraper object with the provided NewsDataFrame and keywords.

        scrape(self) -> list[NewsInfo]:
            Abstract method to be implemented by subclasses for scraping news information.
    """

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    keywords = None

    articles = []
    
    def __init__(self, df: NewsDataFrame, keywords):
        """
        Initializes a Scraper object with the provided NewsDataFrame and keywords.

        Parameters:
            df (NewsDataFrame): The NewsDataFrame object to store the scraped news information.
            keywords: The keywords to be used in the scraping process.
        """
        self.df = df
        self.keywords = keywords

    def scrape(self) -> list[NewsInfo]:
        """
        Abstract method to be implemented by subclasses for scraping news information.

        Returns:
            list[NewsInfo]: A list of NewsInfo objects containing the scraped news information.
        """
        raise NotImplementedError(
            "The 'scrape' method must be implemented by subclasses.")
