import os
import pandas as pd
import chromadb
import uuid

__import__('sqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('sqlite3')

class Portfolio:
    def __init__(self, file_path=None):
        if file_path is None:
            # Get the absolute path to the CSV file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "source", "resource", "my_portfolio.csv")
        
        print(f"Loading portfolio from: {file_path}")  # Debugging line
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])