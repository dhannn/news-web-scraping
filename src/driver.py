from news.news_df import NewsDataFrame
from saver.pdf_saver import PDFSaver
from scraper.inquirer_scraper import InquirerScraper
from scraper.manila_times_scraper import ManilaTimesScraper

"""
The driver script to scrape news information from different sources,
aggregate the data, and save it to CSV, JSON, and PDF formats.
"""

# Initialize a NewsDataFrame to store the scraped news information
news_df = NewsDataFrame() 

# Create a list of Scraper instances for different news sources
scrapers = [
    ManilaTimesScraper(news_df, ['global-warming', 'climate-change']), 
    InquirerScraper(news_df, ['global-warming', 'climate-change'])
    ]

# Iterate through each Scraper instance and execute the scrape method
for scraper in scrapers:
    scraper.scrape()

# Save the aggregated news information to CSV and JSON formats
news_df.save()

# Initialize a PDFSaver to save news information in PDF format
pdf_saver = PDFSaver(news_df.df)
pdf_saver.save()
