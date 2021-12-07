from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class BlockUser(Model):
    __table_name__ = 'block_user'
    block_id = columns.UUID(primary_key=True)
    user_id = columns.TimeUUID(primary_key=True)
    created_at = columns.DateTime()
    role = columns.Text()
    status = columns.Text()
    updated_at = columns.DateTime()