from SimpleNewsScraper import SimpleNewsScraper
from TextProcessor import TextProcessor

scraper = SimpleNewsScraper()
# retrieve news links from meinbezirk.at
scraper.parse_news_links(max_number_articles=2)
# scrape texts from retrieved links
scraper.text_scraping()

processor = TextProcessor(raw_articles=scraper.raw_articles)
processor.tokenize_to_list_of_sentences()

# preprocessing of texts
processor.create_basic_substituion_list()
processor.preprocess_sentences()

# load tagger
processor.specify_hannover_tagger()

# lemmatize
processor.lemmatize_sentences()

# read synonyms dictionary
processor.read_open_thesaurus()

# postprocessing and synonym finding
processor.postprocess_sentences()

# csv report generation
processor.create_csv_report()
