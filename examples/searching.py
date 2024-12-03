import numpy as np
from sklearn.preprocessing import normalize

from DbManage.db_handler import DbHandler
from ImageHandle.vectorizer import Vectorizer


db_handler = DbHandler()
vectorizer = Vectorizer()

tags = ["кот", "луна", "космос", "звёзды"]

file_vector = np.mean([vectorizer.get_vector(tag) for tag in tags], axis=0)
normalized_vector = normalize(file_vector.reshape(1, -1))[0]

print(db_handler.search_nearest(normalized_vector, 3))