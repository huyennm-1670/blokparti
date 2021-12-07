from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Friend(Model):
    __table_name__ = 'friends'
    user_id = columns.UUID(primary_key=True)
    friend_id = columns.UUID(primary_key=True)
    status = columns.Text()
    created_at = columns.DateTime()
    updated_at = columns.DateTime()
