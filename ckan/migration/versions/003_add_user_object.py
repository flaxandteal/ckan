# encoding: utf-8

from sqlalchemy import *
from migrate import *
from ..metadata import CkanMetaData
import uuid


def make_uuid():
    return unicode(uuid.uuid4())


def upgrade(migrate_engine):
    metadata = CkanMetaData()
    user_table = Table('user', metadata,
            Column('id', UnicodeText, primary_key=True, default=make_uuid),
            Column('name', UnicodeText),
            Column('apikey', UnicodeText, default=make_uuid)
            )
    metadata.bind = migrate_engine
    apikey_table = Table('apikey', metadata, autoload=True)

    user_table.create()
    apikey_table.drop()

def downgrade(migrate_engine):
    raise NotImplementedError()

