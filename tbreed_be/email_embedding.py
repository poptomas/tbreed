import re
import pickle
import time
import pandas as pd
import spacy
from utils import benchmark


class EmailPreprocessor:
    def __init__(self, additional_stopwords=None):
        self.additional_stopwords = additional_stopwords or [
            "subject", "fwd", "sent", "cc", "quot", "enron", "ect@ect",
            "hou", "houston", "ees@ees", "texas", "thanks", "thank",
            "original", "forwarded", "message", "email", "attached"
        ]
        self.nlp = spacy.load("en_core_web_md", disable=["ner"])

    def _clean_enron_email(self, email_text):
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            re.IGNORECASE | re.MULTILINE
        )
        email_text = re.sub(url_pattern, '', email_text)

        email_address_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            re.IGNORECASE
        )
        email_text = re.sub(email_address_pattern, '', email_text)

        email_text = re.sub(r'[^\w. ]', '', email_text)
        return email_text.strip()

    @benchmark
    def _preprocess_email(self, text) -> str:
        text = self._clean_enron_email(text)
        doc = self.nlp(text)

        filtered_tokens = [
            str(token.text) for token in doc
            if not (token.is_stop or token.text.lower() in self.additional_stopwords)
        ]

        email = "'" + " ".join(filtered_tokens) if filtered_tokens else "<empty>" + "'"
        return email

    @benchmark
    def preprocess_emails(self, dataframe: pd.DataFrame):
        texts = dataframe["document"].tolist()
        emails = []
        for i, text in enumerate(texts):
            print(i, end=" ")
            r = self._preprocess_email(text)
            emails.append(r)
        return emails

class EmailEmbeddingsService:
    def __init__(self, vectorizer_model, preproc, in_constants):
        self.vectorizer_model = vectorizer_model
        self.preprocessor = preproc
        self.constants = in_constants

    def generate_embeddings(self, email_count: int, email_truncation: int, seed: int):
        df = pd.read_csv(self.constants["emails_fname"], engine="c")
        sampled = df.sample(email_count, random_state=seed)

        # Truncate to the very first `email_truncation` characters
        sampled["document"] = sampled["document"].apply(lambda row: row[:email_truncation])
        sampled.to_csv(self.constants["sampled_fname"], index=False)

        emails = list(self.preprocessor.preprocess_emails(sampled))
        print(len(emails))
        s = time.time()
        created_embeddings = self.vectorizer_model.vectorize(emails)
        output_df = pd.DataFrame(pd.Series(emails), columns=["document"])
        output_df.to_csv(self.constants["sampled_preprocessed_fname"], index=False)
        t = time.time()
        print(f"Embedding time: {t - s:.2f} s")

        with open(self.constants["embeddings_fname"], "wb") as f:
            pickle.dump(created_embeddings, f)

        return {"status": "success"}
