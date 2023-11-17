from sentence_transformers import SentenceTransformer

class Vectorizer:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def vectorize(self, sentences: list[str]):
        return self.model.encode(sentences, show_progress_bar=True)
    
v = Vectorizer("all-MiniLM-L12-v2")

import pandas as pd
emails = pd.read_csv("enron_emails.csv", engine="c")

sample = list(emails["document"].sample(1000, random_state=0))

pica = v.vectorize(sample)

# email similarity
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

def calculate_cosine_similarity(embeddings):
    return cosine_similarity(embeddings, embeddings)

cos_sim = calculate_cosine_similarity(pica)
# show for each of the emails the most similar email

for i, row in enumerate(cos_sim):
    similar_indices = row.argsort()[:-2:-1]
    print(f"Email {i} is most similar to email {similar_indices[1]}") # 0 is the email itself

# email clustering