import numpy as np
from sklearn.preprocessing import normalize

from DbManage.db_handler import DBHandler
from DbManage.vdb_handler import VDBHandler
from FSWatch.Observer import FileSystemWatcher
from ImageHandle.tagger import Tagger
from ImageHandle.vectorizer import Vectorizer


notice_method = lambda event_type, src_path, dest_path: print(event_type, src_path, dest_path)

fw = FileSystemWatcher(notice_method)
dbh = DBHandler()
vdbh = VDBHandler()
v = Vectorizer()
tagger = Tagger()

for file in fw.get_current_files():
    file_id = dbh.new_file(file)
    if file_id is not None:
        tags = tagger.generate_desc(file)
        file_vector = np.mean([v.get_vector(tag) for tag in tags], axis=0)
        normalized_vector = normalize(file_vector.reshape(1, -1))[0]
        vdbh.add_vector(file_id, normalized_vector)

tags = ["кот", "луна", "космос", "звёзды"]

file_vector = np.mean([v.get_vector(tag) for tag in tags], axis=0)
normalized_vector = normalize(file_vector.reshape(1, -1))[0]

print(vdbh.search_nearest(normalized_vector, 3))

del vdbh