API = 'X2TT8uoEK4TsZSrxs5DVBB24sKebajjTHirZbNo98243OVZ3Ha8IPztLm0B7tJhd'
import requests
import json
url = "https://us-east-1.aws.data.mongodb-api.com/app/data-iiery/endpoint/data/v1/action/findOne"

payload = json.dumps({
    "collection": "bim",
    "database": "bim",
    "dataSource": "bim",
    "projection": {
        "_id": 1
    }
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'X2TT8uoEK4TsZSrxs5DVBB24sKebajjTHirZbNo98243OVZ3Ha8IPztLm0B7tJhd',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
