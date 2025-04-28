from peewee import Model, CharField, AutoField
from playhouse.sqlite_ext import JSONField

from DbManage import db

class File(Model):
    """Model representing a file in the database.

    Attributes:
        id (int): The primary key for the file.
        full_path (str): The full path of the file.
    """    
    id = AutoField(primary_key=True)
    full_path = CharField(max_length=1024)
    tags = JSONField(null=True)

    class Meta:
        database = db
