import os

from constants import DB_PATH
from DbManage import db
from DbManage.models import File

class DBHandler:
    def __init__(self):
        """Initializes the DBHandler, connects to the database and creates tables if needed."""
        self.db = db
        if not os.path.exists(DB_PATH):
            self.db.connect()
            self.db.create_tables([File])
        else:
            self.db.connect()

    def new_file(self, full_path: str, file_id: int|None = None) -> int|None:
        """
        Creates a new file record in the database or updates the full path if it already exists.

        Args:
            full_path (str): The full path of the file.
            file_id (int, optional): The ID of the file. Defaults to None.

        Returns:
            int | None: The ID of the created file if it was newly created, otherwise None.
        """
        if file_id:
            file, created = File.get_or_create(
                id=file_id,
                defaults={'full_path': full_path}
            )
            if not created:
                file.full_path = full_path
                file.save()
        else:
            file, created = File.get_or_create(full_path=full_path)
        return file.id if created else None

    def delete_file(self, full_path: str) -> int|None:
        """
        Deletes a file record from the database.

        Args:
            full_path (str): The full path of the file to be deleted.

        Returns:
            int | None: The ID of the deleted file if it existed, otherwise None.
        """
        try:
            deleted_file_id = File.select(File.id).where(File.full_path == full_path).get().id
            File.delete().where(File.id == deleted_file_id).execute()
            return deleted_file_id
        except File.DoesNotExist:
            return None

    def update_file(self, old_path: str, new_path: str) -> int:
        """
        Updates the file path in the database.

        Args:
            old_path (str): The current path of the file.
            new_path (str): The new path to update the file to.

        Returns:
            int: ID of updated file.
        """
        file_id = File.select(File.id).where(File.full_path == old_path).get().id
        File.update(full_path=new_path).where(File.full_path == old_path).execute()
        return file_id
    
    def update_file_tags(self, tags, file_id=None, file_path=None):
        if file_id:
            File.update(tags=tags).where(File.id == file_id).execute()
        elif file_path:
            File.update(tags=tags).where(File.full_path == file_path).execute()

    def get_file_tags(self, file_id) -> list:
        return File.select(File.tags).where(File.id == file_id).get().tags

    def get_id_by_filepath(self, file_path: str) -> int | None:
        """
        Retrieves the file id from the database by file path.

        Args:
            file_path (str): The absolute path of the file.

        Returns:
            id | None: The ID of the file if it exists, otherwise None.
        """
        try:
            return File.select(File.id).where(File.full_path == file_path).get().id
        except File.DoesNotExist:
            return None
        
    def get_filepath_by_id(self, file_id: int) -> str | None:
        """
        Retrieves the file path from the database by file ID.

        Args:
            file_id (int): The ID of the file.

        Returns:
            str | None: The full path of the file if it exists, otherwise None.
        """
        try:
            return File.select(File.full_path).where(File.id == file_id).get().full_path
        except File.DoesNotExist:
            return None
