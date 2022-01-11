from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.types import Type, Field, list_of
from sgqlc.types.relay import Connection, connection_args
from sgqlc.operation import Operation

class DatabaseId(Type):
    id = str
    type = str

class Query(Type):  # GraphQL's root
    database_id = Field(DatabaseId, args={'globalId': str})

def get_global_id(global_id):
    url = 'https://st-api.blokparti.es/v10/graphql'
    # Generate an operation on Query, selecting fields:
    op = Operation(Query)
    # select a field, here with selection arguments, then another field:
    issues = op.database_id(globalId=global_id)
    endpoint = RequestsEndpoint(url)
    data = endpoint(op)
    repo = (op + data).database_id
    id_ = repo.id
    return id_

if __name__ == "__main__":
    print(get_global_id("QWNjb3VudDpjMTU2Njc0ZTU2NzUxMWVjYTM1OGQyNWJjMDU5OTRlZQ=="))