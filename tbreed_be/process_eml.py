from load_dataset import CSVLoader
import email
from utils import benchmark
import pandas as pd
from constants import load_constants

constants = load_constants()

class DatasetProcessor:
    def __init__(self):
        self.df = pd.read_csv(constants["csv_fname"], engine="c")
    
    def __call__(self):
        documents = self.df.apply(self.process_row, axis=1)
        result_df = pd.DataFrame(documents, columns=["document"])
        result_df.to_csv(constants["emails_fname"], index=False)

    #@benchmark
    def process_row(self, row):
        msg = email.message_from_string(row["message"])
        payload = msg.get_payload()
        # remove newlines from the payload
        payload = payload.replace("\n", " ")
        return payload
