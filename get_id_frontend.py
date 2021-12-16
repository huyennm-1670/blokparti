import requests
import json
import pandas as pd

query = """query {
  databaseId(globalId: "QWNjb3VudDpiZmUzZDIxZTA0Y2UxMWVjYmIxZjM3YjJiZjYzNTY1MA==") {
    type
    id
  }
}"""


url = 'https://st-api.blokparti.es/v10/graphql'
r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)


json_data = json.loads(r.text)

id_ = json_data['data']['databaseId']['id']
print(id_)