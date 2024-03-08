# Web Scraping from Local Philippine News Sources

This Python script scrapes information from local news sources such as 
Inquirer and Manila Times.

## Installation
1. Make sure you have Python installed. You can download it from 
[python.org](https://www.python.org/downloads/).
1. Run the command `pip install -r requirements.txt`.

## Usage
1. Simply run the command `py src/driver.py`.
1. Any error is logged in `log/log.txt`.
1. The scraped data is saved in the `data/*` directory.
    - The PDFs format of each record is stored in the `data/pdfs` directory.
    - The aggregated information (both in CSV and JSON) is stored in
    `data/` directory.

## Extending Functionality
1. To scrape more news sources, create a subclass of `Scraper` 
for the particular news source.
    - The `Scraper` class takes in a `pandas DataFrame` that stores the 
    scraped information and a list of keywords.
1. Override the `scrape()` method. 
    - Since different websites have different HTML structures, there is no 
    one correct way to implement the method. However, when working with 
    relatively static, paginated websites, it is advisable to use `requests` 
    to fetch the HTML files and `BeautifulSoup` to parse and extract specific
    information. <br><br> When working with dynamic websites that require more client-
    specific interactions, it is recommeneded to use `Selenium`.

    - The method should use the `self.keywords` attribute as search queries 
    and the `self.df` (which is a `DataFrame` object) attribute to store 
    the information.
1. In the `scrape()` method, once you get the necessary information for one
new story, create a `NewsInfo` object that stores the keyword, date, headline,
byline, section and the content.
1. Add the `NewsInfo` object to the `DataFrame` object by calling the 
`self.df.add_news()` method.
    - The `NewsInfo` requires the following in its constructor: 
        - keyword: str
        - date: str
        - headline: str
        - byline: str
        - section: str
        - content: str
    - Make sure to add the source prefix in the `NewsDataFrame` object
    and initialize the source count to zero.
1. For any errors, log it in the `log/err.txt` file.
1. Go to the main `driver.py` script and add the newly-created class to 
the `scrapers` variable.

## Contact Information
Should there be inquiries about the code or the project, contact me at
[daniel_ramos@dlsu.edu.ph](mailto:daniel_ramos@dlsu.edu.ph). 
Expect a reply within two days. If there is no reply within the timeframe,
feel free to follow up.
