import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from constants import TRACKED_DIRECTORY
from FSWatch.models import EventType
from FSWatch.utils import is_image

class DirectoryEventHandler(FileSystemEventHandler):
    def __init__(self, notice_method):
        self.notice_method = notice_method

    def is_correct_file_type(self, filepath):
        return is_image(filepath)

    def on_modified(self, event):
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.MODIFIED, event.src_path, event.dest_path)
    
    def on_created(self, event):
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.CREATED, event.src_path, event.dest_path)
    
    def on_moved(self, event):
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.MOVED, event.src_path, event.dest_path)
    
    def on_deleted(self, event):
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.DELETED, event.src_path, event.dest_path)

class FileSystemWatcher:
    def __init__(self, notice_method):
        self.observer = Observer()
        self.observer.schedule(DirectoryEventHandler(notice_method), TRACKED_DIRECTORY, recursive=True)
        try:
            self.observer.start()
        except FileNotFoundError:
            exit(1)

    def get_current_files(self):
        file_list = []
        for root, _, files in os.walk(TRACKED_DIRECTORY):
            for file in files:
                file_path = Path(os.path.join(root, file)).absolute()
                file_list.append(file_path)
        return list(filter(is_image, file_list))


    def __del__(self):
        self.observer.stop()
        self.observer.join()