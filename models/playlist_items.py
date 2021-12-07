from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class PlaylistItem(Model):
    __table_name__ = 'playlist_items'
    playlist_id = columns.UUID(primary_key=True, clustering_order="DESC")
    id = columns.TimeUUID(primary_key=True)
    order_rank = columns.Text()
    data_source_id = columns.UUID()
    source_playlist_id = columns.UUID()
    cover_url = columns.Text() # made from data source or track image
