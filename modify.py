import pandas as pd
import vectorizer
import pickle

df = pd.read_csv("enron_emails.csv", engine="c")

model = vectorizer.SentenceTransformerVectorizer(model_name="all-MiniLM-L12-v2")
embeddings = model.vectorize(df["document"])

with open("enron_embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)