import os
from peewee import SqliteDatabase

from constants import DB_PATH

VECTOR_DIMENSION = 300

db = SqliteDatabase(DB_PATH)