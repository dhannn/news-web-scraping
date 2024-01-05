from news.news_df import NewsDataFrame
from saver.pdf_saver import PDFSaver
from scraper.inquirer_scraper import InquirerScraper

news_df = NewsDataFrame()
scraper = InquirerScraper(news_df)
scraper.scrape()
news_df.save()

pdf_saver = PDFSaver(news_df.df)
pdf_saver.save()
