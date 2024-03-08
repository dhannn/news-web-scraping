import pandas as pd

from news.news_info import NewsInfo


class NewsDataFrame:
    """
    Represents a DataFrame for storing news information.

    Attributes:
        df (pandas.DataFrame): The DataFrame to store news information.
        source_count (dict): A dictionary to keep track of the count of news articles from different sources.
        SOURCE_TO_PREFIX (dict): A dictionary mapping full news source names to their respective prefixes.

    Methods:
        __init__(self):
            Initializes a NewsDataFrame object with an empty DataFrame and source count.
            
        add_news(self, news_source, news_info: NewsInfo, subtype=None):
            Adds news information to the DataFrame.

        save(self):
            Saves the DataFrame to CSV and JSON files in the './data/' directory.
    """
    df = None
    source_count = {
        'INQ': 0,
        'MAT': 0
    }

    SOURCE_TO_PREFIX = {
        'Inquirer': 'INQ',
        'Manila Times': 'MAT'
    }

    def __init__(self):
        """
        Initializes a NewsDataFrame object with an empty DataFrame and source count.
        """
        self.df = pd.DataFrame(columns=['keyword', 'headline', 'published_date', 'byline', 'section', 'word_count', 'content'])

    def add_news(self, news_source, news_info: NewsInfo, subtype = None):
        """
        Adds news information to the DataFrame.

        Parameters:
            news_source (str): The source of the news article.
            news_info (NewsInfo): An instance of the NewsInfo class containing the news information.
            subtype (str): An optional subtype to categorize news articles.

        Raises:
            ValueError: If the provided news_source is not recognized.
        """
        prefix = self.SOURCE_TO_PREFIX[news_source]
        count = self.source_count[prefix]
        count += 1

        if subtype is None:
            ctrl_num = '{}-{:05d}'.format(prefix, count)
        else: 
            ctrl_num = '{}{}-{:05d}'.format(prefix, subtype, count)

        self.df.loc[ctrl_num] = [
            news_info.keyword,
            news_info.headline, 
            news_info.date, 
            news_info.byline, 
            news_info.section, 
            news_info.word_count, 
            news_info.content
        ]

        self.source_count[prefix] = count
    
    def save(self):
        """
        Saves the DataFrame to CSV and JSON files in the './data/' directory.
        """
        self.df.to_csv('./data/news_info.csv')
        self.df.to_json('./data/news_info.json')
