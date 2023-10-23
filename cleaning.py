import spacy


class DataCleaner:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_md')
        self.stop_words = self.nlp.Defaults.stop_words

    def remove_stop_words(self, text):
        return [word for word in text if word not in self.stop_words]
    