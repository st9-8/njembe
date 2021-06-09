from peewee import (
	SqliteDatabase,
	Model,
	CharField,
	DateTimeField,
	TextField,
	IntegerField,
	BooleanField,
	ForeignKeyField
)
from njembe.config import EXPORT_FOLDER

import os
import datetime

dbname = os.path.join(EXPORT_FOLDER, '.njembe.db')
db = SqliteDatabase(dbname)

class BaseModel(Model):
	class Meta:
		database = db


class Documentation(BaseModel):
	title = CharField()
	created_date = DateTimeField(default=datetime.datetime.now)
	steps = IntegerField(default=0)
	closed = BooleanField(default=False)


class Step(BaseModel):
	documentation = ForeignKeyField(Documentation)
	command = CharField()
	description = TextField(null=True)
	position = IntegerField(default=0)
