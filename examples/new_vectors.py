import numpy as np
from sklearn.preprocessing import normalize

from DbManage.vdb_handler import VDBHandler
from ImageHandle.vectorizer import Vectorizer

db_handler = VDBHandler()
vectorizer = Vectorizer()

tags_packets = [
    ["кот", "фотоаппарат", "кусать", "объектив", "кошка"],
    ["обезьяна", "кричать", "природа", "удивление"],
    ["солнце", "закат", "одуванчик"],
]

for i, tags in enumerate(tags_packets):
    file_vector = np.mean([vectorizer.get_vector(tag) for tag in tags], axis=0)
    normalized_vector = normalize(file_vector.reshape(1, -1))[0]
    db_handler.add_vector(i, normalized_vector)