from pandas import Series, DataFrame
from saver.saver import Saver
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class PDFSaver(Saver):
    def __init__(self, df: DataFrame):
        self.df = df
    
    def save(self):
        map(PDFSaver.__save, self.df)
        for index, row in self.df.iterrows():
            self.__save(row)
    
    def __save(self, series: Series):
        ctrl_num = series.name
        keyword = series['keyword']
        headline = series['headline']
        byline = series['byline']
        published_date = series['published_date']
        section = series['section']
        content = series['content']
        word_count = series['word_count']

        filename = './data/pdfs/{}.pdf'.format(ctrl_num)
        doc = SimpleDocTemplate(filename)
        story = []

        c = canvas.Canvas(filename)
        story.append(Paragraph(f'Keyword: { keyword }'))
        story.append(Spacer(1,0.1*inch))
        story.append(Paragraph(f'Headline: { headline }'))
        story.append(Spacer(1,0.1*inch))
        story.append(Paragraph(f'Byline: { byline }'))
        story.append(Spacer(1,0.1*inch))
        story.append(Paragraph(f'Published Date: { published_date }'))
        story.append(Spacer(1,0.1*inch))
        story.append(Paragraph(f'Section: { section }'))
        story.append(Spacer(1,0.1*inch))
        story.append(Paragraph(f'Word Count: { word_count }'))
        story.append(Spacer(1,0.1*inch))
        story.append(Paragraph('Content:'))
        story.append(Spacer(1,0.1*inch))
        
        for para in content:
            style = ParagraphStyle(name='normal')
            style.defaults['alignment'] = TA_JUSTIFY
            p = Paragraph(para, style=style)
            story.append(p)
            story.append(Spacer(1,0.2*inch))
        doc.build(story, onLaterPages=PDFSaver.laterPages)
    
    def laterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.restoreState()
