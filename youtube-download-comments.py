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
        print(self.youtube)
        #return self.youtube


    def get_channel_videos(self):
        """Get uploads playlist id"""
        print("get_channel_videos")
        self.res = self.youtube.channels().list(id=self.channel_id,
            part='contentDetails').execute()
        #print(self.res)

        playlist_id = self.res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        #print("Playlist ID=", playlist_id)

        next_page_token = None

        while True:
            self.res = self.youtube.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50, pageToken=next_page_token).execute()
            #print(self.res)
            self.videos += self.res['items']

            next_page_token = self.res.get('nextPageToken')

            if next_page_token is None:
                break

        #print("VIDEOS=",self.videos)
        return self.videos


    def save_desc(self):
        ''' Offer choice to save the acutal **VIDEO Descriptions** '''
        desc_dic = {}
        for idx, video in enumerate(self.videos):
            try:
                print(video['snippet']['title'])
                print(video['snippet']['description'])
                print(video['snippet']['resourceId']['videoId'])

                d_items = ([("id", video['snippet']['resourceId']['videoId']),
                            ("title", video['snippet']['title']),
                            ("description",video['snippet']['description'])])

                desc_dic[idx] = (d_items)
            except:
                pass

        with open("desc.json", 'w') as json_file:
            json.dump(desc_dic,json_file)

    def request_comments(self):
        ls = []
        # Add code here to read desc.json, get videoID and iterate through
        # responses and parse EACH response
        with open("desc.json", 'r') as json_file:
            video_data =json.load(json_file)
            #pprint(video_data)

        for k,v in video_data.items():
            myvideo_id=(v[0][1])

        #for video in video_id:

            #print("request_comments")
            request = self.youtube.commentThreads().list(
                part="snippet,replies",
                videoId=myvideo_id
            )
            response = request.execute()
            pprint(response)
            self.response =  response
            return self.response
            self.parse()


# Parse the res from the API request
    def parse(self):
        print("function PARSE OK")
        content = {}
        full_content = []
        res = self.response

        print(res)

        # Get the number keys and number of ACTUAL comments (exc replies)
        for key in res.keys():
            print (key)
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

                writer.writerow({
                    'comment': content['comment'],
                    'publishedAt': content['publishedAt'],
                    'authorDisplayName': content['authorDisplayName'],
                    'likeCount': content['likeCount']
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
    #Y.parse()
