import os
from pathlib import Path
from typing import Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from constants import TRACKED_DIRECTORY
from FSWatch.models import EventType
from FSWatch.utils import is_image

class DirectoryEventHandler(FileSystemEventHandler):
    """Handles file system events and triggers the specified notice method."""
    def __init__(self, notice_method: Callable[[EventType, str, str], None]) -> None:
        """
        Initializes the event handler with a notice method.

        Args:
            notice_method (callable): The method to call for handling events.
        """
        self.notice_method = notice_method

    def is_correct_file_type(self, filepath: str) -> bool:
        """
        Checks if the file is of the correct type.

        Args:
            filepath (str): The path to the file.

        Returns:
            bool: True if the file is of the correct type, False otherwise.
        """
        return is_image(filepath)

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handles the modified event for files.

        Args:
            event (FileSystemEvent): The event object containing event information.
        """
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.MODIFIED, event.src_path, event.dest_path)

    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handles the created event for files.

        Args:
            event (FileSystemEvent): The event object containing event information.
        """
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.CREATED, event.src_path, event.dest_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        """
        Handles the moved event for files.

        Args:
            event (FileSystemEvent): The event object containing event information.
        """
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.MOVED, event.src_path, event.dest_path)

    def on_deleted(self, event: FileSystemEvent) -> None:
        """
        Handles the deleted event for files.

        Args:
            event (FileSystemEvent): The event object containing event information.
        """
        if self.is_correct_file_type(event.src_path):
            self.notice_method(EventType.DELETED, event.src_path, event.dest_path)

class FileSystemWatcher:
    """
    Monitors the file system for changes.

    Args:
        notice_method (Callable[[EventType, str, str], None]): The method to call for handling events.
    """

    def __init__(self, notice_method: Callable[[EventType, str, str], None]) -> None:
        """Initializes the FileSystemWatcher with a notice method."""
        self.observer = Observer()
        self.observer.schedule(DirectoryEventHandler(notice_method), TRACKED_DIRECTORY, recursive=True)
        try:
            self.observer.start()
        except FileNotFoundError:
            exit(1)

    def get_current_files(self) -> list[Path]:
        """Returns a list of all files in the tracked directory and its subdirectories."""
        file_list = []
        for root, _, files in os.walk(TRACKED_DIRECTORY):
            for file in files:
                file_path = Path(os.path.join(root, file)).absolute()
                file_list.append(file_path)
        return list(filter(is_image, file_list))


    def __del__(self) -> None:
        """Stops and joins the observer thread."""
        self.observer.stop()
        self.observer.join()
