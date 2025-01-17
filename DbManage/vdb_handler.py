import faiss
import numpy as np
from pathlib import Path

from constants import INDEX_PATH
from DbManage import VECTOR_DIMENSION

class VDBHandler:
    def __init__(self) -> None:
        """
        Initializes the VDBHandler.

        If the index file exists, it reads the index from the file.
        Otherwise, it creates a new index.
        """
        if Path(INDEX_PATH).exists():
            self.index = faiss.read_index(INDEX_PATH)
        else:
            self.index = faiss.IndexIDMap(faiss.IndexFlatL2(VECTOR_DIMENSION))

    def __del__(self) -> None:
        """
        Destructor for VDBHandler.

        Writes the index to a file upon deletion.
        """
        faiss.write_index(self.index, INDEX_PATH)

    def add_vector(self, vector_id: int, vector: np.ndarray) -> None:
        """
        Adds a vector to the index.

        Args:
            vector_id (int): The ID of the vector.
            vector (np.ndarray): The vector to add.
        """
        self.index.add_with_ids(vector.reshape(1, -1), np.array([vector_id], dtype='int64'))

    def remove_vector(self, vector_id: int) -> None:
        """
        Removes a vector from the index.

        Args:
            vector_id (int): The ID of the vector to remove.
        """
        self.index.remove_ids(np.array([vector_id], dtype='int64'))

    def search_nearest(self, query_vector: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        """
        Searches for the nearest vectors to a query vector.

        Args:
            query_vector (np.ndarray): The query vector.
            k (int): The number of nearest neighbors to search for.

        Returns:
            tuple: A tuple containing distances and indices of the nearest vectors.
        """
        query_vector = query_vector.reshape(1, -1)
        distances, indices = self.index.search(query_vector, k)
        return distances[0], indices[0]

    def clear_index(self) -> None:
        """
        Clears the index of all vectors and removes the index file if it exists.
        """
        d = self.index.d
        del self.index
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(d))
        if Path(INDEX_PATH).exists():
            Path(INDEX_PATH).unlink()

    def get_all_vectors(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Retrieves all vectors and their IDs from the index.

        Returns:
            tuple: A tuple containing all vectors and their corresponding IDs.
        """
        n = self.index.ntotal
        d = self.index.d
        base_index = getattr(self.index, 'index', self.index)
        all_vectors = np.empty((n, d), dtype='float32')
        all_ids = np.arange(n)

        if hasattr(base_index, 'xb'):
            all_vectors = base_index.xb
        elif hasattr(base_index, 'reconstruct_n'):
            all_vectors = base_index.reconstruct_n(0, n)
        else:
            dummy_query = np.zeros((1, d), dtype='float32')
            _, all_vectors = self.index.search(dummy_query, n)

        return all_vectors, all_ids
