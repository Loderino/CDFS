from DbManage.vdb_handler import VDBHandler
from VectorHandle.vectorizer import Vectorizer

db_handler = VDBHandler()
vectorizer = Vectorizer()

tags_packets = [
    ["кот", "фотоаппарат", "кусать", "объектив", "кошка"],
    ["обезьяна", "кричать", "природа", "удивление"],
    ["солнце", "закат", "одуванчик"],
]

for i, tags in enumerate(tags_packets):
    file_vector = vectorizer.get_set_vector(tags, aggregation_method="mean")
    file_vector.normalize()
    db_handler.add_vector(i, file_vector.value)