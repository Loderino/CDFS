import time
from pathlib import Path

from DbManage.db_handler import DBHandler
from FSWatch.Observer import FileSystemWatcher
from FSWatch.models import EventType

dbh = DBHandler()

def notice_method(event_type, src_path, dest_path):
    if event_type == EventType.CREATED:
        dbh.new_file(Path(src_path).absolute())
        print(f"запись о файле {Path(src_path).absolute()} создана")
    elif event_type == EventType.DELETED:
        dbh.delete_file(Path(src_path).absolute())
        print(f"запись о файле {Path(src_path).absolute()} удалена")
    elif event_type == EventType.MODIFIED:
        dbh.update_file(Path(src_path).absolute(), Path(dest_path).absolute())
        print(f"запись о файле {Path(src_path).absolute()} изменена")
    elif event_type == EventType.MOVED:
        dbh.update_file(Path(src_path).absolute(), Path(dest_path).absolute())
        print(f"запись о файле {Path(src_path).absolute()} перемещена")

fw = FileSystemWatcher(notice_method)
while True:
    time.sleep(1)