import requests
from bs4 import BeautifulSoup

class SimpleNewsScraper():
    def __init__(self):
        self.links = []
        self.raw_articles = []
        pass

    def parse_news_links(self, max_number_articles=10):
        url = r'https://www.meinbezirk.at/tag/engerwitzdorf'
        r = requests.get(url)
        print("Status code: {}".format(r.status_code))
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find_all('article', {})
        # get links to scrape from html text
        for article in articles:
            article_url = article.find('a').get('href')
            self.links.append(article_url)
        if len(self.links) > max_number_articles:
            self.links = self.links[:max_number_articles]
        print("Parsed article links: ")
        print(self.links)
        print("----------------------------------------------------------------")

    def text_scraping(self):
        for article_link in self.links:
            raw = requests.get(article_link)
            raw_soup = BeautifulSoup(raw.text, 'html.parser')
            parsed_article_raw = raw_soup.find('div', {'id': 'content-main'}).find('div')
            texts_in_html = parsed_article_raw.find_all('p')
            full_text = ''
            for text in texts_in_html:
                full_text += text.text + ' '
            self.raw_articles.append(str(full_text))
            # remove duplicates
            self.raw_articles = list(dict.fromkeys(self.raw_articles))
