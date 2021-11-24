import pandas as pd
from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster

cluster = Cluster(connect_timeout=30)
cluster.connection_class = LibevConnection
session = cluster.connect()
session.set_keyspace("v10_stg")

# keyspace: v10_stg for staging and v10_prod for prod
session.set_keyspace("v10_stg")

query = "SELECT * FROM users LIMIT 10"
rows = session.execute(query).all()

df = pd.DataFrame(rows)
cluster.shutdown()
df.to_csv("users.csv", encoding="utf-8")
