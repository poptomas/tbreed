# Text Based Retrieval on Enron Email Dataset


## Setup

### 1) Download Python 3.11+
#### Linux
The procedure is demonstrated on Ubuntu (the author used WSL Ubuntu 22.04)
```
sudo apt -y update
sudo apt -y install software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt -y install python3.11
sudo apt -y install python3.11-venv
alias python=python3.11  # (optional) to simplify the scripts, otherwise, for instance, python3.9 enron_experiment.py [args] is required
```
Taken from https://www.linuxcapable.com/how-to-install-python-3-11-on-ubuntu-linux/
#### Windows
For instance, Python 3.11 can be downloaded from https://www.python.org/downloads/release/python-3114/
venv comes with the installer


### 2) Virtual Environment
highly recommended
to avoid libraries version conflicts
Note that all scripts shown use the "aliased" version of Python (python3.* instead should work out too)
All concrete versions with libraries needed are obtained using the commands below (in terminal):

#### Linux
```
python -m venv venv
source venv/bin/activate
pip install -e .
```

#### Windows
```
python -m venv venv
venv\Scripts\activate
pip install -e .
```

### 3) Download node.js + running Front-end

Visit: https://nodejs.org/en - download LTS recommended
The frontend of the application is running on React via [ViteJS](https://vitejs.dev/guide/).

```
npm install -g create-vite
create-vite tbreed_fe --template react # (or any other name instead of tbreed_fe) 
cd tbreed_fe && npm run dev
```

After that, something similar should appear to ensure that the app frontend is running on port 5173:
```
> tbreed_fe@0.0.0 dev
> vite


  VITE v5.1.1  ready in 443 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 4) Launch Python back-end
The script is located in `tbreed_be` directory:

```
python tbreed_be/entrypoint.py
```

After that, something similar should appear to ensure that the app backend is running on port 5000:
```
 * Serving Flask app 'entrypoint'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 491-529-461
```
At this moment, the application is ready to serve the user for retrieval purposes

### 5) Navigate the application
More or less - there are three options to choose from:
`Download dataset` - necessary step at the very first launch of the application (warning - very slow) - not needed to run unless the input dataset changes - in case of Enron - never
`Embed emails` - necessary step at the very first launch of the application (warning - very slow) - not needed to run unless the seed is changed or the number of emails to embed increases
`Run experiment`
- even though still not very responsive with less than 10 000 emails the processing in a matter of seconds
- the experiment is gradually showing "checkpoints" after each tenth of the job done - new clustering is performed with that amount of processed emails
  - with 10 000 emails - at 1000, 2000, 3000 processed emails there are created records of Bokeh environment to explore emails
  - when hovering the dots in the grid, emails are displayed, and their associated keywords within the cluster the email was assigned to
  
## Warning regarding the application
- since all operations stated above are slow, the application can appear unresponsive
- Expected times for completion:
  - downloading the dataset takes approximately 15-20 minutes
  - embedding of emails for 100 000 emails is expected to run around 10 minutes
  - with 10 000 emails visualizing gradually 1000 (approx. 10 seconds), 2000, ..., 10 000 (approx. 1 minute) emails
  - with 100 000 emails visualizing gradually 10 000, 20 000, ..., 100 000 emails (beware of potential memory limits at approx. 80k+)

Note that with increasing number of emails, the clustered keywords may be more accurate, on the other hand, more general. It was observed that with low amount of emails, on the other hand, the false positive rate regarding keywords can be rather high - 10 000+ is a reasonable amount of emails to make it reasonably accurate.

## Data Preprocessing
Data preprocessing/cleaning is necessary to ensure the emails are less noisy (in case of Enron, still after cleaning, the emails are still rather noisy...). 
To avoid unnecessary processing of extremely large emails (quite frequently encountered on Enron), it was suitable to truncate each email to the very first 1 000 characters (also a useful by-product for visualization of emails to truncate it). Furthermore, URLs and email addresses are removed from the email (just their representation for following embedding). Moreover, English stopwords are removed from the emails including "Enron dataset-specific" stopwords encountered after multiple iterations of visualizing that clusters and observing the clustered keywords using [spaCy medium model](https://spacy.io/models/en#en_core_web_md). Stemming/lemmatization was not taken into consideration due to its extensive computational heaviness - although it is available via spaCy too. 

## Embedding
The embedding of the emails plays the crucial role for the eventual clustering & visualization part.
There have been three methods used: sentence-transformers, word2vec, doc2vec.

### Sentence transformers
[SentenceTransformers](https://www.sbert.net/) is an initially used method in this project (it was initially used on production sentences encountered in email traffic). Even though for clustering purposes, it serves as a very reasonable method for embedding, in this project (as the goal is to capture the meaning of the entire email), it did not prove to be that beneficial as on the sentence-level - it is fairly possible that it was rather necessary to explore various models provided by the library, though.

### Doc2Vec
Another option that came as a reasonable alternative, was to utilize Word2Vec, respectively [Doc2Vec](https://cs.stanford.edu/~quocle/paragraph_vector.pdf) - suitable for vector representations of documents rather than words. Eventually, this method was used in the final application since it provided reasonable embeddings.

## Clustering and Visualization
K-Means with 100 centroids is utilized - further adjustments to be done. Vector dimensionality reduction for 2D visualization purposes used is [UMAP](https://umap-learn.readthedocs.io/en/latest/). Multiple methods have been "tried and tested" - PCA, TSNE, nevertheless, UMAP seemed to spread the vectors in the 2D space in the most reasonable way - PCA seems to direct the vectors in a "line" for most of the inputs, for instance - which is not desirable since there are parts in the space are irregularly distributed. With a large amount of emails, the [Bokeh](https://bokeh.org/) hovertool can´t distinguish between particular emails.

For visualization + exploration of the 2D space filled with emails, Bokeh was utilized
- On the frontend, there is an html frame embedded in the application (eventually not working)
- Bokeh is displayed on the frontend using JS

## Cluster Keywords
Keywords are taken from the emails within the cluster as an input. In this context, emails are considered documents, so on a cluster-level TF-IDF can take place. Another option that has been tried initially on sentences from production emails, was to utilize [TextRank](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf) (available as a pipeline in spaCy - [pytextrank](https://spacy.io/universe/project/spacy-pytextrank) is required). Probably due to the nature of the dataset (noisy Enron), a simpler method, TF-IDF, proved to provide more stable results. Moreover, TF-IDF is much faster.