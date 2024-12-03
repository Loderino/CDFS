import faiss
import numpy as np
from pathlib import Path

from constants import INDEX_PATH
from DbManage import VECTOR_DIMENSION

class DbHandler:
    def __init__(self):
        if Path(INDEX_PATH).exists():
            self.index = faiss.read_index(INDEX_PATH)
        else: 
            self.index = faiss.IndexIDMap(faiss.IndexFlatL2(VECTOR_DIMENSION))

    def add_vector(self, vector_id, vector):
        self.index.add_with_ids(vector.reshape(1, -1), np.array([vector_id], dtype='int64'))

    def search_nearest(self, query_vector, k):
        query_vector = query_vector.reshape(1, -1)
        distances, indices = self.index.search(query_vector, k)
        return distances[0], indices[0]

    def __del__(self):
        faiss.write_index(self.index, INDEX_PATH)
