from pathlib import Path
from PIL import Image

from DbManage.db_handler import DBHandler
from DbManage.vdb_handler import VDBHandler
from FSWatch.models import EventType
from FSWatch.Observer import FileSystemWatcher
from ImageHandle.tagger import Tagger
from VectorHandle.vectorizer import Vectorizer

Image.MAX_IMAGE_PIXELS = None

dbh = DBHandler()
vdbh = VDBHandler()
v = Vectorizer()
tagger = Tagger()

def notice_method(event_type, src_path, dest_path):
    if event_type == EventType.CREATED:
        file_id = dbh.new_file(Path(src_path).absolute())
        print(f"запись о файле {Path(src_path).absolute()} создана с id {file_id}")
        if file_id:
            tags = tagger.generate_desc(src_path)
            file_vector = v.get_set_vector(tags, aggregation_method="mean")
            file_vector.normalize()
            vdbh.add_vector(file_id, file_vector.value)
    elif event_type == EventType.DELETED:
        file_id = dbh.delete_file(Path(src_path).absolute())
        if file_id:
            vdbh.remove_vector(file_id)
            print(f"запись о файле {Path(src_path).absolute()} удалена")
    elif event_type == EventType.MODIFIED:
        file_id = dbh.update_file(Path(src_path).absolute(), Path(dest_path).absolute())
        vdbh.remove_vector(file_id)
        tags = tagger.generate_desc(src_path)
        file_vector = v.get_set_vector(tags, aggregation_method="mean")
        file_vector.normalize()
        vdbh.add_vector(file_id, file_vector.value)
        print(f"запись о файле {Path(src_path).absolute()} изменена")
    elif event_type == EventType.MOVED:
        dbh.update_file(Path(src_path).absolute(), Path(dest_path).absolute())
        print(f"запись о файле {Path(src_path).absolute()} перемещена")

fw = FileSystemWatcher(notice_method)

for ind,file in enumerate(fw.get_current_files()):
    file_id = dbh.new_file(file)
    if file_id is not None:
        print(file_id, file)
        tags = tagger.generate_desc(file)
        if not tags:
            tags = ["loss"]
        file_vector = v.get_set_vector(tags, aggregation_method="mean")
        file_vector.normalize()
        vdbh.add_vector(file_id, file_vector.value)
    if ind >= 300:# для быстрого тестирования
        break

try:
    while True:
        tags = input("Введите теги через пробел: ").split()
        if not tags:
            continue
        file_vector = v.get_set_vector(tags, aggregation_method="mean")
        file_vector.normalize()
        destiny, ids = vdbh.search_nearest(file_vector.value, 5)
        for file_id in ids:
            print(dbh.get_filepath_by_id(file_id))
except (KeyboardInterrupt, EOFError):
    del vdbh
