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


def handle_new_file(path) -> None:
    """
    Processes a newly created file.

    Args:
        path (str): The full path of the new file.
    """
    file_id = dbh.new_file(path)
    if file_id:
        print(f"запись о файле {path} создана с id {file_id}")
        tags = tagger.generate_desc(path)
        file_vector = v.get_set_vector(tags, aggregation_method="mean")
        file_vector.normalize()
        vdbh.add_vector(file_id, file_vector.value)

def handle_removed_file(path):
    """
    Processes a removed file.

    Args:
        path (str): The full path of the removed file.
    """
    file_id = dbh.delete_file(path)
    if file_id:
        vdbh.remove_vector(file_id)
        print(f"запись о файле {path} удалена")

def handle_updated_file(src_path, dest_path):
    """
    Processes an updated file by updating its path in the database and refreshing its vector representation.

    Args:
        src_path (str): The original path of the file.
        dest_path (str): The new path of the file after the update.
    """
    file_id = dbh.update_file(src_path, dest_path)
    vdbh.remove_vector(file_id)
    tags = tagger.generate_desc(dest_path)
    file_vector = v.get_set_vector(tags, aggregation_method="mean")
    file_vector.normalize()
    vdbh.add_vector(file_id, file_vector.value)
    print(f"запись о файле {Path(src_path).absolute()} изменена")

def handle_moved_file(src_path, dest_path):
    """
    Handles the event of a file being moved by updating its path in the database.

    Args:
        src_path (str): The original path of the file before it was moved.
        dest_path (str): The new path of the file after it has been moved.
    """
    dbh.update_file(src_path, dest_path)
    print(f"запись о файле {Path(src_path).absolute()} перемещена")

def notice_method(event_type, src_path, dest_path):
    if event_type == EventType.CREATED:
        handle_new_file(Path(src_path).absolute())
    elif event_type == EventType.DELETED:
        handle_removed_file(Path(src_path).absolute())
    elif event_type == EventType.MODIFIED:
        handle_updated_file(Path(src_path).absolute(), Path(dest_path).absolute())
    elif event_type == EventType.MOVED:
        handle_moved_file(Path(src_path).absolute(), Path(dest_path).absolute())

fw = FileSystemWatcher(notice_method)

for ind, file in enumerate(fw.get_current_files()):
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
