# SimpleTextMining
This is a simple Text Mining Application to scrape and process news articles
from meinbezirk.at.

Install requirements.txt file to be able to execute the pipeline. Example.py
shows how to use this application. If you want to process different articles, you need
to save the texts into a list of lists, where each lists holds one text. Then,
you use the newly created list as an input for TextProcessor.

create_csv_report in TextProcessor generates a report which holds all raw and
processed sentences plus additional information. Overall, there will be
five columns that hold the following information:
- Raw Sentence
- Preprocessed Sentence (removed/substituted special characters)
- Lemmatized Sentence
- Word tags for each word in a sentence
- Synonyms for each word in a sentence