
Clustering Tool – Hierarchical Clustering Web App
Overview
The Clustering Tool is a Flask-based web application that allows users to upload CSV datasets and perform Hierarchical Clustering with automated preprocessing and dendrogram visualization.

This tool is ideal for quick data exploration, grouping similar data points, and visualizing cluster relationships without writing a single line of code.

Features
CSV Upload – Import your dataset directly through the browser.

Automatic Preprocessing – Handles text encoding, missing values, and scaling.

Hierarchical Clustering – Uses Ward’s method for grouping.

Dendrogram Visualization – Automatically generates a dendrogram image for analysis.

Cluster Assignment – Returns the dataset with a new Cluster column.

Tech Stack
Backend: Python, Flask

Data Processing: pandas, scikit-learn, scipy

Visualization: matplotlib

Frontend: HTML templates (Flask render_template)

Installation
Clone the repository
bash
Copy
Edit
git clone https://github.com/madhumitha781/clustering-tool.git
cd clustering-tool
Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Usage
Run the Flask app
bash
Copy
Edit
python app.py
By default, it runs at http://127.0.0.1:5000.

Upload your CSV
Go to the homepage.

Choose your CSV file.

Enter the number of clusters (≥ 2).

Submit and view the dendrogram & clustered data.

App encodes categorical columns, scales data, and performs clustering.

View the dendrogram to analyze relationships.

Download results with assigned cluster labels.

Notes
The CSV must contain at least one numeric column (categorical columns will be encoded automatically).

Large datasets may take longer to process.

Ensure the CSV has a header row.

License
This project is licensed under the MIT License – you are free to use, modify, and distribute.
