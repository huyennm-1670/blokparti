from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class User(Model):
    __table_name__ = 'users'
    id = columns.TimeUUID(primary_key=True)
    account_id = columns.UUID()
    bio = columns.Text()
    cover_image_uri = columns.Text()
    icon_uri = columns.Text()
    resized_icon_uri = columns.Text()
    label = columns.Text()
    updated_at = columns.DateTime()
    username = columns.Text()
    valid = columns.TinyInt()
    vocation_id = columns.TinyInt()