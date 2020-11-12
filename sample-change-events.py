import requests
import json
from datetime import datetime
from datetime import timedelta
from pytz import timezone

#VARIABLES

#Change event integration keys
buildkite_key = ""
github_key= ""
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



#PAYLOADS

#mimicked from screenshots in integration guide
buildkite_payload = { 
  "routing_key": buildkite_key,
  "payload": {
    "summary": "[Passed] Merge pull request #42 from Thursday-Shop/checkout-svc",
    "source": "buildkite/deploy",
    "timestamp": timestamp,
    "custom_details": {
      "author": "{\"email\": \"shoffman@pagerduty.com\", \"name\": \"Sarah Hoffman\"}",
      "branch": "master",
      "commit": "67f0f374-c236-44d8-a968-221c05c1915c",
      "creator": "{\"email\": \"shoffman@pagerduty.com\", \"name\": \"Sarah Hoffman\"}",
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


#mimicked based on what is exposed from real event sent from github
github_payload = { 
  "routing_key": github_key,
  "payload": {
    "summary": "shoffman pushed branch main from thursday-shop/checkout",
    "source": "GitHub",
    "timestamp": timestamp,
    "custom_details": {
      "commits": {"0": "{\"added\":[],\"author\":{\"email\":\"35748040+pdt-shoffman@users.noreply.github.com\",\"name\":\"pdt-shoffman\",\"username\":\"pdt-shoffman\"},\"message\":\"Adding GitHub event\",\"modified\":[\"sample-change-events.py\"],\"removed\":[],\"url\":\"https://github.com/pdt-shoffman/thursday-jam-checkout/commit/6c518def61e9b07eeb9780aa36aba32f1ff6cf0f\"}"},
      "number_of_commits": 1
      
    }
  },
  "links": [
    {
      "href": "https://github.com/pagerduty/",
      "text": "View on GitHub"
    },
    {
      "href": "https://github.com/pagerduty/",
      "text": "Repo"
    },
    {
      "href": "https://github.com/pagerduty/",
      "text": "Sender - shoffman"
    }
  ]
}


#mimicked based on what is exposed from real event sent from gitlab
gitlab_payload = { 
  "routing_key": gitlab_key,
  "payload": {
    "summary": "[Merged - Checkout Service] Fixed bug calculating cart total",
    "source": "GitLab",
    "timestamp": timestamp,
    "custom_details": {
      "body": "Resolved bug reported in ticket CHK-917",
      "repo": "Checkout Service"
      
    }
  },
  "links": [
    {
      "href": "https://gitlab.com/pagerduty/",
      "text": "View on GitLab"
    }
  ]
}



relay_payload = { 
  "routing_key": relay_key,
  "payload": {
    "summary": "Puppet run for master-srf03-sfprod",
    "timestamp": timestamp,
    "source": "puppet",
    "custom_details": {
    }
  }
}



#SEND EVENTS
buildkite_response = requests.request("POST", url, headers=headers,data=json.dumps(buildkite_payload))
print(buildkite_response.text)

github_response = requests.request("POST", url, headers=headers,data=json.dumps(github_payload))
print(github_response.text)

gitlab_response = requests.request("POST", url, headers=headers,data=json.dumps(gitlab_payload))
print(gitlab_response.text)

relay_response = requests.request("POST", url, headers=headers,data=json.dumps(relay_payload))
print(relay_response.text)