from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Account(Model):
    __table_name__ = 'accounts'
    id = columns.TimeUUID(primary_key=True)
    email = columns.Text()
    date_of_birth = columns.Date()
    inviter_id = columns.UUID()
    phone = columns.Text()
    password = columns.Text()
    registration_tokens = columns.Set(value_type=columns.Text())
    salt = columns.Text()
    updated_at = columns.DateTime()
    valid = columns.TinyInt()