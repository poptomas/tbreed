def load_constants():
    path = "."
    return {
        "tar_gz_fname": f"{path}/enron.tar.gz",
        "csv_fname": f"{path}/enron.csv",
        "dataset_dir": f"{path}/maildir",
        "embeddings_fname": f"{path}/enron_embeddings.pkl",
        "emails_fname": f"{path}/enron_emails.csv",
        "sampled_fname": f"{path}/enron_sampled.csv",
        "sampled_preprocessed_fname": f"{path}/enron_sampled_preprocessed.csv",
    }