from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class UserSession(Model):
    __table_name__ = 'user_sessions'
    id = columns.TimeUUID(primary_key=True)
    user_id = columns.UUID()
    account_id = columns.UUID()
    device_uid = columns.Text()
    expires_at = columns.DateTime()