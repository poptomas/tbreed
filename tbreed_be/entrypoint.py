from flask import Flask, render_template, request
from flask_cors import CORS
from sklearn.cluster import KMeans

import spacy
import umap
import pandas as pd
from constants import load_constants

from email_embedding import EmailPreprocessor, EmailEmbeddingsService
from enron_download import Enron
from process_eml import DatasetProcessor
import vectorizer
from cluster_analyzer import EmailClusterAnalyzer

import re
import os
import pickle


constants = load_constants()
app = Flask(__name__)

CORS(app=app)


@app.route('/download', methods=['POST'])
def download():
    enron = Enron(
        tar_fname=constants["tar_gz_fname"],
        csv_fname=constants["csv_fname"],
        ds_fname=constants["dataset_dir"]
    )
    if not os.path.exists(constants["dataset_dir"]):
        os.makedirs(constants["dataset_dir"])
    url = "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz"
    enron.download_dataset(url, chunk_size=1024)
    enron.unzip_dataset()
    enron.build_csv()
    DatasetProcessor()()
    enron.clean_up()
    return {
        "status": "success"
    }


@app.route('/embeddings', methods=['POST'])
def embeddings():
    raw_data = request.get_json()
    value_count = int(raw_data["value"])
    seed = int(raw_data["seed"])
    truncation = 1000

    preprocessor = EmailPreprocessor()
    vectorizer_model = vectorizer.Doc2VecVectorizer("doc2vec")
    email_embeddings_service = EmailEmbeddingsService(vectorizer_model, preprocessor, constants)

    result = email_embeddings_service.generate_embeddings(value_count, truncation, seed)
    return result


@app.route('/visualize', methods=['POST'])
def visualize():
    
    def get_embeddings():
        with open(constants["embeddings_fname"], "rb") as f:
            return pickle.load(f)
        
    def check_file_existence(*files):
        return all(os.path.exists(file_path) for file_path in files)

    if not check_file_existence(
            constants["sampled_fname"],
            constants["sampled_preprocessed_fname"],
            constants["embeddings_fname"]
        ):
        return {"status": "error"}
    
    raw_data = request.get_json()
    email_count = int(raw_data["value"])
    visualization_iteration = int(raw_data["iteration"])
    print(raw_data)
    
    dimred_model = umap.UMAP(random_state=0)
    cluster_count = 100

    model = KMeans(n_clusters=cluster_count, random_state=0, n_init="auto")
    nlp = spacy.load("en_core_web_md", disable=["ner"])

    original_emails_df = pd.read_csv(constants["sampled_fname"], nrows=email_count)
    preproc_emails_df = pd.read_csv(constants["sampled_preprocessed_fname"], nrows=email_count)
    em_embeddings = get_embeddings()

    email_visualizer = EmailClusterAnalyzer(
        model=model,
        dimred_model=dimred_model,
        nlp=nlp
    )
    result = email_visualizer.perform_clustering(
        emails=original_emails_df["document"],
        prep_emails=preproc_emails_df["document"],
        embeddings=em_embeddings,
        vis_value=visualization_iteration
    )
    return result


if __name__ == '__main__': 
    app.run(debug=True)