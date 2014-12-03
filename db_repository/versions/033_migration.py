from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('current_player_id', Integer),
    Column('settup_round', Boolean),
    Column('started', Boolean, default=ColumnDefault(False)),
    Column('colors_left', PickleType),
    Column('buildings', PickleType),
    Column('roads', PickleType),
    Column('hexes', PickleType),
    Column('probabilities', PickleType),
    Column('robber_location', PickleType),
    Column('largest_army_player_id', Integer),
    Column('longest_road_player_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].columns['colors_left'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].columns['colors_left'].drop()
