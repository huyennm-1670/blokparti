from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class PartyPlayedItem(Model):
    __table_name__ = 'party_played_items'
    party_id = columns.UUID(primary_key=True)
    played_at = columns.DateTime(primary_key=True, clustering_order="ASC")
    cover_url = columns.Text()
    data_source_id = columns.UUID()
    id = columns.UUID()
    order_rank = columns.Text()
    playlist_id = columns.UUID()
    source_playlist_id = columns.UUID()
    updated_at = columns.DateTime()