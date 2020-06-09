from peewee import Model
from peewee import SqliteDatabase
from peewee import CharField
from peewee import IntegerField

db = SqliteDatabase('database.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    external_id = IntegerField()
