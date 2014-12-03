from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
player = Table('player', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('color', INTEGER, nullable=False),
    Column('devcards', BLOB),
    Column('cities', BLOB),
    Column('settlements', BLOB),
    Column('roads', BLOB),
    Column('largest_army', BOOLEAN),
    Column('knights_played', INTEGER, nullable=False),
    Column('longest_road', BOOLEAN, nullable=False),
    Column('longest_road_len', INTEGER, nullable=False),
    Column('game_id', INTEGER),
    Column('user_id', INTEGER),
    Column('resources', BLOB),
    Column('order', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['player'].columns['color'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['player'].columns['color'].create()
