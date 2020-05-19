#!/usr/bin/python
# -*- coding: utf-8 -*-
# Extract comments youtube.comments.list per video
# Run with API Key in separate file
# Source from :
# https://developers.google.com/explorer-help/guides/code_samples#python
# redandgreen.co.uk

''' Check GitHub for additions https://github.com/RGGH/rng'''

import os
from pprint import pprint
import googleapiclient.discovery
import json
import csv
from API_Key import myapi

def banner():
    print("******************************")
    print("****  YouTube Comments    ****")
    print("******************************")

class Ycom(object):
    def __init__(self):
        self.video_id = ""
        self.ytcom = ""
        self.ytpubat = ""
        self.ytauth = ""
        self.ytlike = ""
        self.data = {}
        #playlist specific
        self.videos = []
        self.channel_id = "UCKyhocQPsAFKEY5REfVoseQ"



    def make_youtube(self):
        print("function make_youtube_object")
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = myapi

        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)


    def get_channel_videos(self):
        """Get uploads playlist id"""
        print("get_channel_videos")
        self.res = self.youtube.channels().list(id=self.channel_id,
            part='contentDetails').execute()

        playlist_id = self.res['items'][0]['contentDetails'] \
            ['relatedPlaylists']['uploads']

        next_page_token = None

        while True:
            self.res = self.youtube.playlistItems().list(
                playlistId=playlist_id,
                part='snippet',
                maxResults=50,
                pageToken=next_page_token).execute()

            self.videos += self.res['items']

            next_page_token = self.res.get('nextPageToken')

            if next_page_token is None:
                break

    def save_desc(self):
        ''' Offer choice to save the acutal **VIDEO Descriptions** '''
        desc_dic = {}
        for idx, video in enumerate(self.videos):
            try:
                #print(video['snippet']['title'])
                #print(video['snippet']['description'])
                print(idx+1, video['snippet']['resourceId']['videoId'])

                d_items = ([("id", video['snippet']['resourceId']['videoId']),
                            ("title", video['snippet']['title']),
                            ("description",video['snippet']['description'])])

                desc_dic[idx] = (d_items)
            except:
                pass

        #pprint(desc_dic)
        with open("desc.json", 'w') as json_file:
            json.dump(desc_dic,json_file,indent=4)

    def request_comments(self):
        ls = []
        # Add code here to read desc.json, get videoID and iterate through
        # responses and parse EACH response
        with open("desc.json", 'r') as json_file:
            video_data =json.load(json_file)

        for k,v in video_data.items():

            self.video_id = (v[0][1])
            #self.video_id = myvideo_id
            try:
                request = self.youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId = self.video_id
                )
                response = request.execute()
                self.response =  response
                #return self.response
                self.parse()
                #print("Parsed")
            except:
                print("Comments Were Disabled for this Video ", self.video_id)
                pass

# Parse the res from the API request - call from 'request_comments'
    def parse(self):
        print("function PARSE OK")
        content = {}
        full_content = []
        res = self.response

        #pprint(res)

        # Get the number keys and number of ACTUAL comments (exc replies)
        for key in res.keys():
            #print (key)
            ncoms =(res['pageInfo']['totalResults'])
            #print(ncoms)

        # Create dict and write each line to CSV
        for i in range(0,ncoms):
            #
            ytcom = (res['items'][i]['snippet']['topLevelComment']
                ['snippet']['textOriginal'])
            ytpubat = (res['items'][i]['snippet']['topLevelComment']
                ['snippet']['publishedAt'])
            ytauth = (res['items'][i]['snippet']['topLevelComment']
                ['snippet']['authorDisplayName'])
            ytlike = (res['items'][i]['snippet']['topLevelComment']
                ['snippet']['likeCount'])
            #
            content['comment'] = ytcom
            content['publishedAt'] = ytpubat
            content['authorDisplayName'] = ytauth
            content['likeCount'] = ytlike
            #
            file_exists = os.path.isfile('comments.csv')
            #
            with open('comments.csv','a') as csvfile:
                headers = [
                    'video_id',
                    'comment',
                    'publishedAt',
                    'authorDisplayName',
                    'likeCount'
                    ]
                writer = csv.DictWriter(csvfile, delimiter=',',
                    lineterminator='\n',
                    fieldnames=headers
                    )

                if not file_exists:
                   writer.writeheader()
                try:
                    writer.writerow({
                        'video_id' : self.video_id,
                        'comment': content['comment'],
                        'publishedAt': content['publishedAt'],
                        'authorDisplayName': content['authorDisplayName'],
                        'likeCount': content['likeCount']
                        })
                except:
                    pass

        #return


# main driver
if __name__ == "__main__":

    banner()
    Y = Ycom()
    Y.make_youtube()
    Y.get_channel_videos()

    Y.save_desc()

    Y.request_comments()
