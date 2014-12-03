from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('settup_round', BOOLEAN),
    Column('started', BOOLEAN),
    Column('buildings', BLOB),
    Column('roads', BLOB),
    Column('hexes', BLOB),
    Column('probabilities', BLOB),
    Column('robber_location', BLOB),
    Column('largest_army_size', INTEGER),
    Column('longest_road_size', INTEGER),
    Column('current_player_id', INTEGER),
    Column('largest_army_player_id', INTEGER),
    Column('longest_road_player_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['largest_army_size'].drop()
    pre_meta.tables['game'].columns['longest_road_size'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['largest_army_size'].create()
    pre_meta.tables['game'].columns['longest_road_size'].create()
