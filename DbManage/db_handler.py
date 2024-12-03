import os

from constants import DB_PATH
from DbManage import db
from DbManage.models import File

class DBHandler:
    def __init__(self):
        self.db = db
        if not os.path.exists(DB_PATH):
            self.db.connect()
            self.db.create_tables([File])
        else:
            self.db.connect()    
    def new_file(self, full_path, file_id=None):
        if file_id:
            File.update(id=file_id, full_path=full_path)
        File.create(full_path=full_path)

    def delete_file(self, full_path):
        try:
            deleted_file_id = File.select(File.id).where(File.full_path == full_path).get().id
            File.delete().where(File.id == deleted_file_id).execute()
            return deleted_file_id
        except File.DoesNotExist:
            return None
        
    def update_file(self, old_path, new_path):
        File.update(full_path=new_path).where(File.full_path == old_path).execute()

    def get_filepath_by_id(self, file_id):
        try:
            return File.select(File.full_path).where(File.id == file_id).get().full_path
        except File.DoesNotExist:
            return None