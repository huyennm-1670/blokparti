from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Playlist(Model):
    __table_name__ = 'playlists'
    id = columns.TimeUUID(primary_key=True)
    creator_id = columns.UUID() # refers to users.id
    updated_at = columns.DateTime()
    title = columns.Text()
    descriptions = columns.Text()
    cover_urls = columns.List(columns.Text()) # made from playlist_items.cover_url
    selected_item_id = columns.UUID()