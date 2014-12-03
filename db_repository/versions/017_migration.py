from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
player = Table('player', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('color', INTEGER, nullable=False),
    Column('brick', INTEGER, nullable=False),
    Column('ore', INTEGER, nullable=False),
    Column('lumber', INTEGER, nullable=False),
    Column('wool', INTEGER, nullable=False),
    Column('grain', INTEGER, nullable=False),
    Column('devcards', BLOB),
    Column('cities', BLOB),
    Column('settlements', BLOB),
    Column('roads', BLOB),
    Column('largest_army', BOOLEAN),
    Column('knights_played', INTEGER, nullable=False),
    Column('longest_road', BOOLEAN, nullable=False),
    Column('longest_road_len', INTEGER, nullable=False),
    Column('user', INTEGER),
    Column('game_id', INTEGER),
)

player = Table('player', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('game_id', Integer),
    Column('color', Integer, nullable=False),
    Column('brick', Integer, nullable=False, default=ColumnDefault(0)),
    Column('ore', Integer, nullable=False, default=ColumnDefault(0)),
    Column('lumber', Integer, nullable=False, default=ColumnDefault(0)),
    Column('wool', Integer, nullable=False, default=ColumnDefault(0)),
    Column('grain', Integer, nullable=False, default=ColumnDefault(0)),
    Column('devcards', PickleType),
    Column('cities', PickleType),
    Column('settlements', PickleType),
    Column('roads', PickleType),
    Column('largest_army', Boolean, default=ColumnDefault(False)),
    Column('knights_played', Integer, nullable=False, default=ColumnDefault(0)),
    Column('longest_road', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('longest_road_len', Integer, nullable=False, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['player'].columns['user'].drop()
    post_meta.tables['player'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['player'].columns['user'].create()
    post_meta.tables['player'].columns['user_id'].drop()
