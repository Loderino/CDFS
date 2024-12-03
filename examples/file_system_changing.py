import time

from FSWatch.Observer import FileSystemWatcher
from FSWatch.models import EventType

def notice_method(event_type, src_path, dest_path):
    print(f'Event type: {EventType(event_type).name}')
    print(f'Source path: {src_path}')
    print(f'Destination path: {dest_path}')

fw = FileSystemWatcher(notice_method)
while True:
    time.sleep(1)