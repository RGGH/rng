#!/usr/bin/python
# coding: utf-8
# Extract comments youtube.comments.list per video
# Run with API Key in separate file called API_Key.py 
# example : https://github.com/RGGH/rng/blob/master/API_Key.py
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
        self.title = ""
        self.description =""
        self.rpcom = ""
        self.rppubat =""
        self.rpauth = ""
        self.rplike = ""
        self.tcomment_count = ""
        self.tdislike_count = ""
        self.tfavorite_count = ""
        self.tlike_count = ""
        self.tview_count = ""

        self.videos = []
        self.channel_id = "UCKyhocQPsAFKEY5REfVoseQ"

        self.response=""



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

    # Get the Video rating for each video in channel
    def get_ratings(self, video_id):
        request = self.youtube.videos().list(
        part="id,  statistics",
        id=video_id
        )
        response = request.execute()

        dx = response
        tp = dx['items'][0]['statistics']

        self.tcomment_count = tp['commentCount']
        self.tdislike_count = tp['dislikeCount']
        self.tfavorite_count = tp['favoriteCount']
        self.tlike_count = tp['likeCount']
        self.tview_count = tp['viewCount']
        return


    def save_desc(self):
        ''' Offer choice to save the acutal **VIDEO Descriptions** '''
        desc_dic = {}
        for idx, video in enumerate(self.videos):
            try:
                print(idx+1, video['snippet']['resourceId']['videoId'])
                self.title = video['snippet']['title']
                self.description = video['snippet']['description']

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

        # Add code here to read desc.json, get videoID and iterate through
        # responses and parse EACH response
        with open("desc.json", 'r') as json_file:
            video_data =json.load(json_file)

        for k,v in video_data.items():

            self.video_id = (v[0][1])
            self.title = (v[1][1])
            self.description = (v[2][1])
            # Get ratings stats ready for CSV
            ratings = self.get_ratings(self.video_id)
            #print ("CC=",self.tcomment_count)

            try:
                request = self.youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId = self.video_id
                )
                res = request.execute()
                self.response =  res
                #return self.response

                #print("Parsed")

                # print(res)
                # for key in res.keys():
                #     ncoms =(res['pageInfo']['totalResults'])
                #
                # for i in range(0,ncoms):
                #     #
                #     self.rpcom = (res['items'][i]['snippet']['topLevelComment']
                #         ['snippet']['textOriginal'])
                #     self.rppubat = (res['items'][i]['snippet']['topLevelComment']
                #         ['snippet']['publishedAt'])
                #     self.rpauth = (res['items'][i]['snippet']['topLevelComment']
                #         ['snippet']['authorDisplayName'])
                #     self.rplike = (res['items'][i]['snippet']['topLevelComment']
                #         ['snippet']['likeCount'])

                self.make_csv()
                print("Adding to csv...",self.video_id)
            except:
                print("No comments Available - Write minimum to csv",self.video_id)
                self.make_csv()
#

# Parse the res from the API request - call from 'request_comments'
    def make_csv(self):
        print("writing to csv ",self.video_id)
        file_exists = os.path.isfile('comments.csv')
        #
        with open('comments.csv','a') as csvfile:
            headers = [
                'video_id',
                'title',
                'description',
                'comment',
                'published_at',
                'author_display_name',
                'comment_like_count',
                'comment_count',
                'video_dislike_count',
                'video_favourite_count',
                'video_like_count',
                'video_view_count'
                ]
            writer = csv.DictWriter(csvfile, delimiter=',',
                lineterminator='\n',
                fieldnames=headers,
                )

            if not file_exists:
               writer.writeheader()
            try:
                #
                writer.writerow({
                    'video_id' : self.video_id,
                    'title': self.title,
                    'description':self.description,
                    'comment': self.rpcom,
                    'published_at': self.rppubat,
                    'author_display_name': self.rpauth,
                    'comment_like_count': self.rplike,
                    'comment_count':self.tcomment_count,
                    'video_dislike_count':self.tdislike_count,
                    'video_favourite_count':self.tfavorite_count,
                    'video_like_count': self.tlike_count,
                    'video_view_count':self.tview_count
                    })
            except:
                #print("Something went wrong when parsing ",self.video_id)
                writer.writerow({
                    'video_id' : self.video_id,
                    'title': self.title,
                    'description':self.description
                    })
        return

# main driver
if __name__ == "__main__":

    banner()
    Y = Ycom()
    Y.make_youtube()
    Y.get_channel_videos()
    Y.save_desc()
    Y.request_comments()
