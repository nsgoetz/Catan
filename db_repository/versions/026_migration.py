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
    Column('game_id', INTEGER),
    Column('user_id', INTEGER),
)

player = Table('player', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('game_id', Integer),
    Column('color', Integer, nullable=False),
    Column('resources', PickleType),
    Column('devcards', PickleType),
    Column('cities', PickleType),
    Column('settlements', PickleType),
    Column('roads', PickleType),
    Column('largest_army', Boolean, default=ColumnDefault(False)),
    Column('knights_played', Integer, nullable=False, default=ColumnDefault(0)),
    Column('longest_road', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('longest_road_len', Integer, nullable=False, default=ColumnDefault(0)),
)

game = Table('game', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
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
    Column('current_player_id', INTEGER),
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
    Column('largest_army_player_id', Integer),
    Column('largest_army_size', Integer, default=ColumnDefault(2)),
    Column('longest_road_player_id', Integer),
    Column('longest_road_size', Integer, default=ColumnDefault(4)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['player'].columns['brick'].drop()
    pre_meta.tables['player'].columns['grain'].drop()
    pre_meta.tables['player'].columns['lumber'].drop()
    pre_meta.tables['player'].columns['ore'].drop()
    pre_meta.tables['player'].columns['wool'].drop()
    post_meta.tables['player'].columns['resources'].create()
    pre_meta.tables['game'].columns['largest_army_player'].drop()
    pre_meta.tables['game'].columns['longest_road_player'].drop()
    post_meta.tables['game'].columns['largest_army_player_id'].create()
    post_meta.tables['game'].columns['longest_road_player_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['player'].columns['brick'].create()
    pre_meta.tables['player'].columns['grain'].create()
    pre_meta.tables['player'].columns['lumber'].create()
    pre_meta.tables['player'].columns['ore'].create()
    pre_meta.tables['player'].columns['wool'].create()
    post_meta.tables['player'].columns['resources'].drop()
    pre_meta.tables['game'].columns['largest_army_player'].create()
    pre_meta.tables['game'].columns['longest_road_player'].create()
    post_meta.tables['game'].columns['largest_army_player_id'].drop()
    post_meta.tables['game'].columns['longest_road_player_id'].drop()
