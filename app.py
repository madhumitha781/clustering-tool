import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # use non-interactive backend for servers
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import StandardScaler, LabelEncoder

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)

def hierarchical_clustering(file_path, num_clusters):
    # load file
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # Basic validation
    if df.shape[0] == 0:
        raise ValueError("Uploaded file is empty.")

    # Keep a copy for display (original text values)
    display_df = df.copy()

    # Encode all object (text) columns using LabelEncoder so everything becomes numeric
    text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    encoders = {}
    for c in text_cols:
        le = LabelEncoder()
        # convert to string to avoid issues and fillna with 'NA'
        df[c] = df[c].astype(str).fillna("NA")
        try:
            df[c] = le.fit_transform(df[c])
            encoders[c] = le
        except Exception:
            # fallback: replace with zeros if encoding fails
            df[c] = 0

    # Now select numeric columns (after encoding everything will be numeric types)
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if len(numeric_cols) == 0:
        raise ValueError("No numeric features available for clustering after encoding.")

    df_numeric = df[numeric_cols].astype(float)

    # Fill any remaining NaNs in numeric columns with column median
    df_numeric = df_numeric.fillna(df_numeric.median())

    # Standardize
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df_numeric)

    # Hierarchical clustering (Ward's method is common)
    Z = linkage(data_scaled, method='ward')

    # Save dendrogram
    dendrogram_path = os.path.join('static', 'dendrogram.png')
    plt.figure(figsize=(12, 6))
    dendrogram(Z, leaf_rotation=90., leaf_font_size=8.)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Sample index")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.savefig(dendrogram_path, dpi=150)
    plt.close()

    # Assign clusters (maxclust: create exactly num_clusters clusters)
    clusters = fcluster(Z, num_clusters, criterion='maxclust')
    display_df['Cluster'] = clusters

    return display_df, dendrogram_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part in request.")
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No file selected.")
        try:
            num_clusters = int(request.form.get('num_clusters', 3))
            if num_clusters < 2:
                return render_template('index.html', error="Number of clusters must be >= 2.")
        except ValueError:
            return render_template('index.html', error="Invalid number of clusters.")
