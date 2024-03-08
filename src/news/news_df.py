import pandas as pd

from news.news_info import NewsInfo


class NewsDataFrame:
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
        self.df = pd.DataFrame(columns=['keyword', 'headline', 'published_date', 'byline', 'section', 'word_count', 'content'])

    def add_news(self, news_source, news_info: NewsInfo):
        prefix = self.SOURCE_TO_PREFIX[news_source]
        count = self.source_count[prefix]
        count += 1

        ctrl_num = '{}-{:05d}'.format(prefix, count)

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

    def add_news(self, news_source, news_info: NewsInfo, subtype = None):
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
        self.df.to_csv('./data/news_info.csv')
        self.df.to_json('./data/news_info.json')
