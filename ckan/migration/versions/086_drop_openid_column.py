# encoding: utf-8

from sqlalchemy import MetaData


def upgrade(migrate_engine):
    metadata = CkanMetaData()
    metadata.bind = migrate_engine
    migrate_engine.execute('''
ALTER TABLE "user"
    DROP COLUMN openid;
    ''')
