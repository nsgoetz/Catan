from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('current_player', INTEGER),
    Column('settup_round', BOOLEAN),
    Column('started', BOOLEAN),
    Column('buildings', BLOB),
    Column('roads', BLOB),
    Column('hexes', BLOB),
    Column('probabilities', BLOB),
    Column('robber_location', BLOB),
    Column('largest_army_player', INTEGER),
    Column('largest_army_size', INTEGER),
    Column('longest_road_player', INTEGER),
    Column('longest_road_size', INTEGER),
)

game = Table('game', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('current_player_id', Integer),
    Column('settup_round', Boolean),
    Column('started', Boolean, default=ColumnDefault(False)),
    Column('buildings', PickleType),
    Column('roads', PickleType),
    Column('hexes', PickleType),
    Column('probabilities', PickleType),
    Column('robber_location', PickleType),
    Column('largest_army_player', Integer),
    Column('largest_army_size', Integer, default=ColumnDefault(2)),
    Column('longest_road_player', Integer),
    Column('longest_road_size', Integer, default=ColumnDefault(4)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['current_player'].drop()
    post_meta.tables['game'].columns['current_player_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['current_player'].create()
    post_meta.tables['game'].columns['current_player_id'].drop()
