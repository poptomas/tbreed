
from sklearn.base import ClusterMixin
import numpy as np
import time
from html import escape
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, save
from bokeh.transform import linear_cmap
from bokeh.palettes import Turbo
from sklearn.feature_extraction.text import TfidfVectorizer
import umap
from bokeh.embed import components
import json
import pandas as pd
import pytextrank
from utils import benchmark
from bokeh.embed import json_item


class EmailClusterAnalyzer:
    def __init__(self, model: ClusterMixin, dimred_model, nlp):
        self.model = model
        self.dimred_model = dimred_model
        self.nlp = nlp
        self.keyword_count = 10

    @benchmark
    def perform_clustering(self, emails, prep_emails, embeddings, vis_value: int):
        vis_truncation = 1000
        embeddings = embeddings[0: len(emails)]
        red_embeddings = self.dimred_model.fit_transform(np.array(embeddings))
        cluster_labels = self.model.fit_predict(red_embeddings)
        emails = [escape(str(email)) for email in emails]
        emails = [email[:vis_truncation] for email in emails]
        prep_emails = [str(email) for email in prep_emails]

        print(f"Clustering: {len(prep_emails)} emails")

        df = pd.DataFrame({
            'cluster_label': cluster_labels,
            'email': prep_emails
        })
        
        cluster_titles = self._generate_titles_using_tfidf(df)
        #cluster_titles = self._generate_titles(df)
        cluster_titles = [cluster_titles[label] for label in cluster_labels]

        x_coords = red_embeddings[:, 0].tolist()
        y_coords = red_embeddings[:, 1].tolist()

        # Create a Bokeh figure
        plot = figure(
            title="Clustered Emails Visualization", 
            x_axis_label=f"Processed emails: {len(prep_emails)}"
        )
        color_mapper = linear_cmap(
            field_name='cluster_label',
            palette=Turbo[256],
            low=min(cluster_labels),
            high=max(cluster_labels)
        )

        # Hover tool
        style = """
            <div style="max-width: 400px;">
                <p style="color: #00008B"><strong>Cluster: </strong>@cluster_label</p>
                <p style="color: #00008B"><strong>Email: </strong>@email</p>
                <p style="color: #00008B"><strong>Cluster Keywords:</strong> @cluster_title</p>
            </div>
        """
        hover = HoverTool(tooltips=style, line_policy="next", point_policy="snap_to_data", mode="mouse")
        plot.add_tools(hover)

        # Create a ColumnDataSource
        source = ColumnDataSource(data={
            'x': x_coords,
            'y': y_coords,
            'cluster_label': cluster_labels,
            'email': emails,
            'cluster_title': cluster_titles
        })
        plot.circle('x', 'y', size=10, source=source, color=color_mapper)
        output_file(f'cluster_visualization{vis_value}.html')
        save(plot)
        div, script = components(plot)
        return {
            "status": "success",
            "email_count": len(prep_emails),
            "visualization_count": vis_value,
            # return html of the plot
            "div": div,
            "script": script,
            "plot": json.dumps(json_item(plot))
        }

    # Using pytextrank - eventually unused
    def _generate_titles(self, cluster_df):
        cluster_titles = []
        min_length = 5
        filtered_ds = sorted(cluster_df['cluster_label'].unique())
        self.nlp.add_pipe("textrank")
        for cluster_label in filtered_ds:
            cluster_sentences = cluster_df[cluster_df['cluster_label'] == cluster_label]['email']
            text = " ".join(list(cluster_sentences))
            doc = self.nlp(text)
            phrases = doc._.phrases
            sorted_phrases = sorted(phrases, key=lambda x: x.rank * x.count, reverse=True)
            # filter phrases that are too short
            sorted_phrases = [phrase for phrase in sorted_phrases if len(phrase.text) >= min_length]
            title = ", ".join([phrase.text for phrase in sorted_phrases][:self.keyword_count])
            cluster_titles.append(title)
        return cluster_titles

    def _generate_titles_using_tfidf(self, cluster_df):
        cluster_titles = []
        min_length = 5
        filtered_ds = sorted(cluster_df['cluster_label'].unique())
        vectorizer = TfidfVectorizer(min_df=1)
        for cluster_label in filtered_ds:
            cluster_emails = list(cluster_df[cluster_df['cluster_label'] == cluster_label]['email'])
            tfidf_matrix = vectorizer.fit_transform(cluster_emails)
            feature_names = vectorizer.get_feature_names_out()

            # Get top phrases based on TF-IDF scores
            term_scores = tfidf_matrix.sum(axis=0)
            top_phrases_idx = np.argsort(np.ravel(term_scores))[::-1]
            top_phrases_idx = top_phrases_idx.tolist()
            top_phrases = [feature_names[idx] for idx in top_phrases_idx if len(feature_names[idx]) >= min_length]
            # filter those that contain numbers - most probably FP
            top_phrases = [phrase for phrase in top_phrases if not any(char.isdigit() for char in phrase)]
            top_phrases = top_phrases[:self.keyword_count]
            title = ", ".join(list(top_phrases))
            cluster_titles.append(title)
        return cluster_titles
