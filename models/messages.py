from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Message(Model):
    __table_name__ = 'messages'
    conversation_id = columns.UUID(primary_key=True)
    id = columns.BigInt(primary_key=True, clustering_order="DESC")
    user_id = columns.UUID()
    content = columns.Text()
    conversation_type = columns.Text()
    edited = columns.Boolean()
    files = columns.List(value_type=columns.Text())
    message_type = columns.Text()
    updated_at = columns.DateTime()
    created_at = columns.DateTime()