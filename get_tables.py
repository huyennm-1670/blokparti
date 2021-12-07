from cassandra.io.libevreactor import LibevConnection
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from models.parties import Party
from models.accounts import Account
from models.auto_playlists import AutoPlaylist
from models.block_user import BlockUser
from models.blocks import Block
from models.friends import Friend
from models.messages import Message
from models.parties import Party
from models.party_played_items import PartyPlayedItem
from models.party_user import PartyUser
from models.playlist_items import PlaylistItem
from models.playlists import Playlist
from models.user_sessions import UserSession
from models.users import User
import pandas as pd
import time

start_time = time.time()

cluster = Cluster(connect_timeout=30)
cluster.connection_class = LibevConnection
session = cluster.connect()

# keyspace: v10_stg for staging and v10_prod for prod
session.set_keyspace("v10_prod")
connection.register_connection('cluster1', session=session)

#get a table
parties = Party.objects.using(keyspace="v10_prod", connection='cluster1').all()
parties_list = []
for party in parties:
    parties_list.append(dict(party))
parties_df = pd.DataFrame.from_records(parties_list)
# parties_df.to_csv("csv_files/accounts.csv", encoding="utf-8")

cluster.shutdown()

print(f"Processing time is {time.time() - start_time}s")