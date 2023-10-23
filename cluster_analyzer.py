
from sklearn.base import ClusterMixin
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models import ColumnDataSource, HoverTool
import bokeh.palettes
import spacy
import pytextrank
import umap


class SentenceClusterAnalyzer:
    def __init__(self, model: ClusterMixin, sents: list[str], embeds: list[str]):
        self.unique_sentences = sents
        self.unique_embeddings = embeds
        self.cluster_labels = None
        self.model = model

    def perform_clustering(self):
        umap_model = umap.UMAP(random_state=42)
        self.umap_embeddings = umap_model.fit_transform(np.array(self.unique_embeddings))
        self.cluster_labels = self.model.fit_predict(self.umap_embeddings)

    def visualize_clusters(self):
        df = pd.DataFrame({
            'cluster_label': self.cluster_labels,
            'sentence': self.unique_sentences
        })

        cluster_titles = self._generate_titles(df)
        print(cluster_titles)
        df['cluster_name'] = [cluster_titles[label] for label in df['cluster_label']]

        #tsne = TSNE(n_components=2, random_state=0, perplexity=self.perplexity)
        #tsne_results = tsne.fit_transform(np.array(self.unique_embeddings))

        plot = figure(width=800, height=600, title="Sentence Clusters Visualization (2D)")

        df['umap_x'] = self.umap_embeddings[:, 0]
        df['umap_y'] = self.umap_embeddings[:, 1]
        palette = bokeh.palettes.turbo(cluster_count)
        df['color'] = [palette[i] for i in df['cluster_label']]
        source = ColumnDataSource(df)

        plot.circle('umap_x', 'umap_y', size=10, color='color', source=source)

        hover = HoverTool()
        hover.tooltips = [
            ("Sentence", "@sentence"),
            ("Cluster Name", "@cluster_name"),
            ("Cluster", "@cluster_label")
        ]
        plot.add_tools(hover)

        output_notebook()
        output_file("visualization.html")

        show(plot)

    def print_clusters(self):
        if self.cluster_labels is not None:
            unique_clusters = sorted(np.unique(self.cluster_labels))
            for cluster in unique_clusters:
                print(f"Cluster {cluster}:")
                sentences_in_cluster = [self.unique_sentences[i] for i, label in enumerate(self.cluster_labels) if label == cluster]
                for sentence in sentences_in_cluster:
                    print(f"- {sentence}")
                print()


    def _generate_titles(self, cluster_df, n_top_phrases=3):
        cluster_titles = []
        nlp = spacy.load("en_core_web_md")
        nlp.add_pipe("textrank")
        for cluster_label in sorted(cluster_df['cluster_label'].unique()):
            cluster_sentences = cluster_df[cluster_df['cluster_label'] == cluster_label]['sentence']
            text = " ".join(cluster_sentences)
            doc = nlp(text)
            phrases = doc._.phrases
            sorted_phrases = sorted(phrases, key=lambda x: x.rank * x.count, reverse=True)
            title = ", ".join([phrase.text for phrase in sorted_phrases][:n_top_phrases])
            cluster_titles.append(title)
        return cluster_titles

