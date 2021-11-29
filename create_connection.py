from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster
import pandas as pd

cluster = Cluster(connect_timeout=30)
cluster.connection_class = LibevConnection
session = cluster.connect()

# keyspace: v10_stg for staging and v10_prod for prod
session.set_keyspace("v10_prod")

tables = [
    "accounts",
    "users",
    "parties",
    "user_sessions",
    "party_user",
    "blocks",
    "block_user",
    # "playlists",
    # "playlist_items",
    # "auto_playlists",
    # "party_played_items",
    # "messages",
    # "countries",
    # "friends",
    # "task_time_marks",
    # "party_boot",
    # "block_building_level",
    "last_activity"
]

for table in tables:
    query = f"SELECT * FROM {table}"
    rows = session.execute(query)
    df = pd.DataFrame(rows)
    # display(df)
    df.to_csv(f"{table}.csv", encoding="utf-8")

cluster.shutdown()
