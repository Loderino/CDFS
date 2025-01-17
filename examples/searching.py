from DbManage.vdb_handler import VDBHandler
from VectorHandle.vectorizer import Vectorizer


vdb_handler = VDBHandler()
vectorizer = Vectorizer()

tags = ["кот", "луна", "космос", "звёзды"]

file_vector = vectorizer.get_set_vector(tags, aggregation_method="mean")
file_vector.normalize()

print(vdb_handler.search_nearest(file_vector.value, 3))