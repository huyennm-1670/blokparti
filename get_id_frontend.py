import requests
import json
import pandas as pd


def get_global_id(label_id: str):
  if label_id is not None or label_id != "":
    query1 = '''query {
    databaseId(globalId: "'''

    query2 = '''") {
        type
        id
      }
    }'''

    query = query1 + label_id + query2

    url = 'https://st-api.blokparti.es/v10/graphql'
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)

    id_ = json_data['data']['databaseId']['id']
  else:
    id_ = None
  return id_

if __name__ == '__main__':
  print(get_global_id("QWNjb3VudDpjMTU2Njc0ZTU2NzUxMWVjYTM1OGQyNWJjMDU5OTRlZQ=="))