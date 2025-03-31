import pandas as pd
import chromadb
import uuid

__import__('sqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('sqlite3')


class Portfolio:
    def __init__(self, file_path = "resource\my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")