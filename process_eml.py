from load_dataset import CSVLoader
import email
from utils import benchmark
import pandas as pd

@benchmark
def process_row(row):
    msg = email.message_from_string(row["message"])
    payload = msg.get_payload()
    # remove newlines from the payload
    payload = payload.replace("\n", " ")
    return payload

l = CSVLoader()
df = l.load_dataset("enron.csv")

documents = df.apply(process_row, axis=1)

result_df = pd.DataFrame(documents, columns=["document"])
result_df.to_csv("enron_emails.csv", index=False)