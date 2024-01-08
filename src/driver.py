from news.news_df import NewsDataFrame
from saver.pdf_saver import PDFSaver
from scraper.inquirer_scraper import InquirerScraper
from scraper.manila_times_scraper import ManilaTimesScraper

news_df = NewsDataFrame()
scraper = ManilaTimesScraper(news_df)
scraper.scrape()
news_df.save()

pdf_saver = PDFSaver(news_df.df)
pdf_saver.save()
