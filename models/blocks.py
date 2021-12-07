from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Block(Model):
    __table_name__ = 'blocks'
    id = columns.TimeUUID(primary_key=True)
    cover_image_uri = columns.Text()
    creator_id = columns.UUID()
    description = columns.Text()
    icon_uri = columns.Text()
    name = columns.Text()
    resized_icon_uri = columns.Text()
    short_id = columns.Text()
    updated_at = columns.DateTime()