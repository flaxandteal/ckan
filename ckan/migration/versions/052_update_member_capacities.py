# encoding: utf-8

from migrate import *
from ckan.model.metadata import CkanMigrationMetaData

def upgrade(migrate_engine):
    migrate_engine.execute("""
    BEGIN;
        UPDATE member SET capacity='public' WHERE capacity='member'
                                            AND table_name='package';
        UPDATE member_revision SET capacity='public' WHERE capacity='member'
                                                     AND   table_name='package';
    COMMIT;
    """
    )
