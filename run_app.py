import numpy as np
from pathlib import Path
from PIL import Image
from sklearn.preprocessing import normalize

from DbManage.db_handler import DBHandler
from DbManage.vdb_handler import VDBHandler
from FSWatch.models import EventType
from FSWatch.Observer import FileSystemWatcher
from ImageHandle.tagger import Tagger
from ImageHandle.vectorizer import Vectorizer

Image.MAX_IMAGE_PIXELS = None

dbh = DBHandler()
vdbh = VDBHandler()
v = Vectorizer()
tagger = Tagger()

def notice_method(event_type, src_path, dest_path):
    if event_type == EventType.CREATED:
        file_id = dbh.new_file(Path(src_path).absolute())
        print(f"запись о файле {Path(src_path).absolute()} создана с id {file_id}")
        tags = tagger.generate_desc(src_path)
        file_vector = np.mean([v.get_vector(tag) for tag in tags], axis=0)
        normalized_vector = normalize(file_vector.reshape(1, -1))[0]
        vdbh.add_vector(file_id, normalized_vector)
    # elif event_type == EventType.DELETED:
    #     dbh.delete_file(Path(src_path).absolute())
    #     print(f"запись о файле {Path(src_path).absolute()} удалена")
    # elif event_type == EventType.MODIFIED:
    #     dbh.update_file(Path(src_path).absolute(), Path(dest_path).absolute())
    #     print(f"запись о файле {Path(src_path).absolute()} изменена")
    # elif event_type == EventType.MOVED:
    #     dbh.update_file(Path(src_path).absolute(), Path(dest_path).absolute())
    #     print(f"запись о файле {Path(src_path).absolute()} перемещена")

fw = FileSystemWatcher(notice_method)

for ind,file in enumerate(fw.get_current_files()):
    file_id = dbh.new_file(file)
    if file_id is not None:
        print(file_id, file)
        tags = tagger.generate_desc(file)
        if not tags:
            tags = ["loss"]
        file_vector = np.mean([v.get_vector(tag) for tag in tags], axis=0)
        normalized_vector = normalize(file_vector.reshape(1, -1))[0]
        vdbh.add_vector(file_id, normalized_vector)
    if ind >= 300:# для быстрого тестирования
        break

try:
    while True:
        tags = input("Введите теги через пробел: ").split()
        if not tags:
            continue
        file_vector = np.mean([v.get_vector(tag) for tag in tags], axis=0)
        normalized_vector = normalize(file_vector.reshape(1, -1))[0]
        destiny, ids = vdbh.search_nearest(normalized_vector, 5)
        for file_id in ids:
            print(dbh.get_filepath_by_id(file_id+1))
except (KeyboardInterrupt, EOFError):
    del vdbh
