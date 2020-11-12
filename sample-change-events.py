import requests
import json
from datetime import datetime
from datetime import timedelta
from pytz import timezone


#Integration keys
buildkite_key = ""
github_key=""
relay_key=""
gitlab_key=""

#Change events endpoint
url = "https://events.pagerduty.com/v2/change/enqueue"

headers = {
    'accept': "application/vnd.pagerduty+json;version=2",
    'content-type': "application/json",
    }


#Gets timestamp for 15 minutes in the past to send in backdated events
today = datetime.now(timezone('UTC'))
timestamp = today.isoformat()
prev_timestamp = today - timedelta(minutes=15)
prev_timestamp_iso = prev_timestamp.isoformat()

#Payloads
buildkite_payload = { 
  "routing_key": buildkite_key,
  "payload": {
    "summary": "[Passed] Merge pull request #42 from Thursday-Shop/checkout-svc",
    "source": "buildkite/deploy",
    "timestamp": timestamp,
    "custom_details": {
    	"author": {"email": "shoffman@pagerduty.com", "name": "Sarah Hoffman"},
    	"branch": "master",
    	"commit": "67f0f374-c236-44d8-a968-221c05c1915c",
    	"creator": {"email": "shoffman@pagerduty.com", "name": "Sarah Hoffman"},
    	"duration": "5m 22s",
    	"id": "3a67b99-d123-839c-dd45-93820c83a2",
    	"number": 7382,
    	"state": "passed"
    }
  },
  "links": [
    {
      "href": "https://buildkite.com/pagerduty/",
      "text": "Build #7382"
    }
  ]
}



#Send in events
response = requests.request("POST", url, headers=headers,data=json.dumps(buildkite_payload))
print(response.text)

