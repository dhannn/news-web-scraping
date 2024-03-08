from saver.saver import Saver


class NewsInfo:

    """
    Represents information about a news article.

    Attributes:
        date (str): The date of the news article.
        headline (str): The headline of the news article.
        byline (str): The byline or author of the news article.
        section (str): The section or category to which the news article belongs.
        content (str): The content or body of the news article.
        word_count (int): The word count of the news article content.

    Methods:
        __init__(self, keyword: str, date: str, headline: str, byline: str, section: str, content: str):
            Initializes a NewsInfo object with the provided information.

        save(self, save: Saver):
            Saves the news information using the provided Saver object.
    """

    date = None
    headline = None
    byline = None
    section = None
    content = None
    word_count = None
    
    
    def __init__(self, keyword: str, date: str, headline: str, byline: str, section: str, content: str):
        """
        Initializes a NewsInfo object with the provided information.

        Parameters:
            keyword (str): The keyword associated with the news article.
            date (str): The date of the news article.
            headline (str): The headline of the news article.
            byline (str): The byline or author of the news article.
            section (str): The section or category to which the news article belongs.
            content (str): The content or body of the news article.
        """
        self.date = date
        self.headline = headline
        self.byline = byline
        self.section = section
        self.content = content
        self.keyword = keyword
        self.word_count = len(' '.join(content).split())

    def save(self, save: Saver):
        """
        Saves the news information using the provided Saver object.

        Parameters:
            save (Saver): An instance of the Saver class responsible for saving news information.
        """
        save.save()
