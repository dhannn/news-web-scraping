from saver.saver import Saver


class NewsInfo:
    date = None
    headline = None
    byline = None
    section = None
    content = None
    word_count = None

    def __init__(self, keyword: str, date: str, headline: str, byline: str, section: str, content: str):
        self.date = date
        self.headline = headline
        self.byline = byline
        self.section = section
        self.content = content
        self.keyword = keyword
        self.word_count = len(' '.join(content).split())

    def save(self, save: Saver):
        save.save()
