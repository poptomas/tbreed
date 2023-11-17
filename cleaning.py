import spacy


class DataCleaner:
    def __init__(self, text):
        self.nlp = spacy.load('en_core_web_md')
        self.stop_words = self.nlp.Defaults.stop_words
        self.text = text

    def remove_stop_words(self):
        self.text = [word for word in self.text if word not in self.stop_words]
        return self

    def lemmatize(self):
        self.text = [token.lemma_ for token in self.text]
        return self