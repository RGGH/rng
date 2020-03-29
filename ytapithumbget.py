#refer to : https://developers.google.com/youtube/v3/docs/videos#resource-representation
# sudo pip install --upgrade google-api-python-client

import requests
import os
from apiclient.discovery import build
import apikey
import time

api_key = apikey.api_key
youtube = build('youtube', 'v3', developerKey=api_key)
channel_id = "UCaylBLE7uSfVYJYjLv74G0Q"

class Ytg(object):

    def __init__(self):
        self.apikey = apikey.api_key
        self.channel_id = channel_id 
        self.spath = "youtube_thumbnails"
        self.sdest  = ""
        self.videos = []
        self.res = youtube.channels().list(id=self.channel_id, 
                                      part='contentDetails').execute()

    # make 'thumbnails' folder in local dir if not already there
    def md(self):
        print(f"checking for {self.spath}")  
        if not os.path.exists(self.spath):
            print("Thumbnails folder does not exist, making it for you")
            time.sleep(1)
            os.makedirs(self.spath)


    # Ask user what to name download folder
    def ask_destd(self):
        self.destd = input("What do you want to name the folder of downloads? ")
        self.destd = self.destd.lower()

        if not os.path.exists(self.spath + "/" + self.destd +"/"):
            time.sleep(1)
            os.makedirs(self.spath + "/" + self.destd +"/")
        return         


    def get_channel_videos(self):

        # Get uploads playlist id
        
        print(self.res)
        playlist_id = self.res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        next_page_token = None

        while True:
            self.res = youtube.playlistItems().list(playlistId=playlist_id, 
                                               part='snippet', 
                                               maxResults=50,
                                               pageToken=next_page_token).execute()
            self.videos += self.res['items']
            print(self.videos)
            next_page_token = self.res.get('nextPageToken')

            if next_page_token is None:
                break
            
        return self.videos

    def process_videos(self):
        #self.videos = get_channel_videos()
        for video in self.videos:
                    print(video['snippet']['title'])
                    #print(video['snippet']['description'])

    def save_thumbs(self): 
        for idx, image in enumerate(self.videos):

                        print(image['snippet']['thumbnails']['high']['url'])
                        url = (image['snippet']['thumbnails']['high']['url'])

                        s_name = url.split('/')[-2]

                        print(s_name)
                        totalvids = (len(self.videos))
                        print(f"Getting thumbnail number,{idx} of {totalvids}")
                        print("*" * idx)
                        r = requests.get(url, allow_redirects=True)

                        open(self.spath + "/" + self.destd + "/" + s_name +".jpg", 'wb').write(r.content)

        print (f"Done, now check you local directory /{self.spath}/{self.destd} for your thumbnails")





# MAIN #

if __name__ == "__main__":

        dls = Ytg()
        dls.md()
        dls.ask_destd()
        dls.get_channel_videos()
        dls.process_videos()
        dls.save_thumbs()

















##        for idx, image in enumerate(self.videos):
##
##                        print(image['snippet']['thumbnails']['high']['url'])
##                        url = (image['snippet']['thumbnails']['high']['url'])
##
##                        s_name = url.split('/')[-2]
##
##                        print(s_name)
##                        totalvids = (len(self.videos))
##                        print(f"Getting thumbnail number,{idx} of {totalvids}")
##                        print("*" * idx)
##                        r = requests.get(url, allow_redirects=True)
##
##                        open(self.spath + "/" + self.destd + "/" + s_name +".jpg", 'wb').write(r.content)
##
##        print (f"Done, now check you local directory /{self.spath}/{self.destd} for your thumbnails")
##


