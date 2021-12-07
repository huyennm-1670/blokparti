from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class AutoPlaylist(Model):
    __table_name__ = 'auto_playlists'
    playlist_id = columns.UUID(primary_key=True)
    started_at = columns.DateTime()
    scheduled_until = columns.DateTime()
    updated_at = columns.DateTime()