# encoding: utf-8

from sqlalchemy import *
from migrate import *
from ..metadata import CkanMetaData
import migrate.changeset

def upgrade(migrate_engine):
    metadata = CkanMetaData()
    metadata.bind = migrate_engine
    for table_name in ['change', 'changemask', 'changeset']:
        table = Table(table_name, metadata, autoload=True)
        table.drop()
