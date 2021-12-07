from uuid import UUID
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class PartyUser(Model):
    __table_name__ = 'party_user'
    party_id = columns.UUID(primary_key=True)
    user_id = columns.UUID(primary_key=True)
    attendance_status = columns.Text()
    created_at = columns.DateTime()
    ext = columns.Map(str, str)
    invitation_code = columns.Text()
    invitee_ids = columns.Set(columns.UUID())
    role = columns.Text()
    updated_at = columns.DateTime()