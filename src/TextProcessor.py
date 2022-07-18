import csv
import re
import nltk
from HanTa import HanoverTagger as ht


class TextProcessor():
    def __init__(self, raw_articles, special_chars_delete=None, special_chars_space=None, substitutions=None):
        """
        :param raw_articles: List of lists of raw article texts.
        :param special_chars_delete: List of characters to delete from article texts.
        :param special_chars_space: List of characters to substitute with whitespace.
        :param substitutions: Dictionary of substitutions for article texts.
        """

        if substitutions is None:
            substitutions = []
        if special_chars_space is None:
            special_chars_space = []
        if special_chars_delete is None:
            special_chars_delete = []
        self.raw_articles = raw_articles
        self.sentences = []
        self.preprocessed_sentences = []
        self.lemma_triplets_sentences = []
        self.special_chars_delete = special_chars_delete
        self.special_chars_space = special_chars_space
        self.substitutions = substitutions

        self.lemmatized_sentences = []
        self.word_stem_tags = []
        self.synonym_sentences = []

        self.synonyms = []

        self.tagger = None

    def specify_hannover_tagger(self):
        nltk.download('punkt')
        self.tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    def create_basic_substituion_list(self):
        """
        Create basic lists for deletion and substitution.
        :return:
        """

        self.special_chars_delete = ['.', '?', '!', ',', '"', '.', ':', ';', '´',
                                     '`', '\'', '„', '“', '-', '(', ')', '’', '@', '/']
        self.special_chars_space = ['\xa0', '\n']
        self.substitutions = {'ä': 'ae', 'Ä': 'Ae', 'Ö': 'Oe', 'ö': 'oe', 'Ü': 'Ue', 'ü': 'ue'}

    def tokenize_to_list_of_sentences(self):
        # tokenize raw text in savable format (list of sentences)
        tokenized_texts_raw = []
        for article in self.raw_articles:
            sentences = nltk.sent_tokenize(article, language='german')
            tokenized_text = [nltk.word_tokenize(sent, language='german')
                              for sent in sentences]
            tokenized_texts_raw.append(tokenized_text)

        for t_text in tokenized_texts_raw:
            for t_sentence in t_text:
                s = ""
                i = 1
                for token in t_sentence:
                    if i < len(t_sentence) and t_sentence[i] != '.':
                        s += token + ' '
                    else:
                        s += token
                i += 1
                self.sentences.append(s.strip())

    def preprocess_sentences(self):
        """
        Use specified lists to preprocess sentences, e.g. remove special characters.
        """

        for i in range(0, len(self.sentences)):
            sentence = self.sentences[i]
            for special_char in self.special_chars_space:
                sentence = sentence.replace(special_char, ' ')
            for k_, v_ in self.substitutions.items():
                sentence = sentence.replace(k_, v_)
            for special_char in self.special_chars_delete:
                sentence = sentence.replace(special_char, ' ')
            # remove redundant whitespaces
            sentence = re.sub(' +', ' ', sentence).strip()
            self.preprocessed_sentences.append(sentence)

    def lemmatize_sentences(self):
        tokenized_text = [nltk.word_tokenize(sent, language='german')
                          for sent in self.preprocessed_sentences]
        self.lemma_triplets_sentences = [self.tagger.tag_sent(tokenized_sentence)
                                    for tokenized_sentence in tokenized_text]

    def read_open_thesaurus(self):
        with open('../resources/openthesaurus.txt', encoding='utf-8') as thesaurus:
            for line in thesaurus.readlines():
                if line[0] != '#':
                    self.synonyms.append(line.split(';'))

    # used to find synonyms for a lemma
    def __add_synonyms_for_lemma_to_dict(self, lemma, synonym_dict):
        for synonyms in self.synonyms:
            if lemma in synonyms:
                synonym_dict[lemma] = synonyms
                break
        return synonym_dict

    def postprocess_sentences(self):
        """
        Split triplets to word tags and lemmas, also find synonyms for each token in a sentence.
        :return:
        """
        for sentence_triplets in self.lemma_triplets_sentences:
            sentence_l = ""
            sentence_t = ""
            synonym_dict = dict()
            for triplet in sentence_triplets:
                sentence_l += triplet[1] + " "
                sentence_t += triplet[2] + " "
                synonym_dict = \
                    self.__add_synonyms_for_lemma_to_dict(triplet[1], synonym_dict)
            self.lemmatized_sentences.append(sentence_l.strip())
            self.word_stem_tags.append(sentence_t)
            self.synonym_sentences.append(synonym_dict)

    def create_csv_report(self):
        with open('../output/output.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Original", "Preprocessed",
                             "Lemmatized", "Tags", "Synonyms"])
            for orig, pre, lemm, tag, syn in zip(self.sentences,
                                                 self.preprocessed_sentences,
                                                 self.lemmatized_sentences,
                                                 self.word_stem_tags,
                                                 self.synonym_sentences):
                writer.writerow([orig, pre, lemm, tag, syn])




