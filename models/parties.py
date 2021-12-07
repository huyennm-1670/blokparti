from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Party(Model):
    __table_name__ = 'parties'
    id = columns.TimeUUID(primary_key=True)
    auience_size = columns.Integer()
    begin_time = columns.DateTime()
    block_id = columns.UUID()
    cover_image_uri = columns.Text()
    creator_id = columns.UUID()
    description = columns.Text()
    dj_setlist = columns.UUID()
    end_time = columns.DateTime()
    icon_uri = columns.Text()
    resized_icon_uri = columns.Text()
    mode = columns.Text()
    name = columns.Text()
    playlist_id = columns.UUID()
    start_time = columns.DateTime()
    status = columns.Text()
    updated_at = columns.DateTime()

