from peewee import Model, CharField, AutoField

from DbManage import db

class File(Model):
    id = AutoField(primary_key=True)
    full_path = CharField(max_length=1024)

    class Meta:
        database = db