#!/usr/bin/python

# Update the snippet metadata for a video. Sample usage:
#   python update_video.py --video_id=<VIDEO_ID> --tags="<TAG1, TAG2>" --title="New title" --description="New description"

#import argparse
import os
import sys
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import json

CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

""" This started from YouTube API documentation - "update_video.py" but has
been rewritten to go with "ytthumbget.py" as the part that updated the
YouTube video descriptions"""

# Ytg = Youtube GET
# Ytp = YouTube PUT

class Ytp(object):
    def __init__(self, fjson="_desc.json"):
        self.fjson = fjson
        self.json_id = ""
        self.json_title = ""
        self.json_description =""

    # Authorize the request and store authorization credentials.
    def get_authenticated_service(self):
      flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
      credentials = flow.run_console()
      return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
    
    def run_json(self):
        with open(self.fjson) as f:
          data = json.loads(f.read())
          for k,v in data.items():
               k = int(k)
               v_id = (v[0])
               des =(v[2])
               self.json_description =(des[1])
               self.json_id= v_id[1]
               print(self.json_id)
               print(self.json_description[:50],"...")
               print("_" * 80)

               videos_list_response = youtube.videos().list(
                   id=self.json_id, part='snippet').execute()
               
               videos_list_snippet = videos_list_response['items'][0]['snippet']
               videos_list_snippet['description'] = self.json_description
               
               videos_update_response = youtube.videos().update(
                   part='snippet',
                   body=dict(
                       snippet=videos_list_snippet,
                       id=self.json_id
                       )).execute()

##  # Since the request specified a video ID, the response only contains one
##  # video resource. This code extracts the snippet from that resource.
##  videos_list_snippet = videos_list_response['items'][0]['snippet']


# MAIN # ----------------------------------------------------------------------------------------

if __name__ == '__main__':

  dlu = Ytp()  
  youtube = dlu.get_authenticated_service()
  dlu.run_json()
