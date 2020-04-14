"""refer to : https://developers.google.com/youtube/v3/docs/videos#resource-representation
    Use : sudo pip install --upgrade google-api-python-client
    You will need your own API key and put it into a new file called 'apikey.py'
    e.g api_key = "xxxxxxxxxxxxxxxxxxxxxx" """

import os
import sys
import json
import time
import apikey
import requests
from tqdm import tqdm
from pytube import Playlist
from pytube import YouTube
from apiclient.discovery import build
from google.auth.transport.requests import Request

channel_id = "UCv_liC5hA3VwwHBxNwa35ug"
api_key = apikey.api_key
youtube = build('youtube', 'v3', developerKey=api_key)
additional_text = ""
    
class Ytg(object):

    def __init__(self):
        self.apikey = apikey.api_key
        self.channel_id = channel_id
        self.video_id = ""
        self.spath = "youtube_downloads"
        self.sdest  = ""
        self.videos = []    
        self.res = youtube.channels().list(id=self.channel_id, 
                                      part='contentDetails').execute()    
        self.full_path = ""
        self.videodl = ""
        self.exc_dl = {}


    def md(self):
        """make 'youtube_downloads' folder in local dir if not already there"""
        print(f"checking for exisiting {self.spath} ")  
        if not os.path.exists(self.spath):
            print("Folder - 'youtube_downloads' - does not exist, making it for you")
            time.sleep(1)
            os.makedirs(self.spath)  
        return


    def list_dir(self): 
        """ List directories inside youtube downloads in case user wants to resume"""
        x = [x for x in os.listdir(self.spath) if os.path.isdir(os.path.join(self.spath, x))]
        if x != [] :
            print (x)
   
    
    def ask_destd(self):
        """Ask user what to name download the subfolder"""
        self.destd = input("What do you want to name the folder of these downloads? ")
        self.destd = self.destd.lower()
        if not os.path.exists(self.spath + "/" + self.destd +"/"):
            time.sleep(1)
            os.makedirs(self.spath + "/" + self.destd +"/")
            self.full_path = (self.spath + "/" + self.destd +"/")
        else: 
            resume = input(f"{self.full_path} !! Folder already exists...do you want to resume previous attempt? y/n")
            if resume.lower() == "y":
                print("Ok. I will carry on and fetch the rest of the videos")
                self.full_path = (self.spath + "/" + self.destd +"/")
            else:
                print("Please start again with a new folder name the old downloads will remain")
                if os.path.exists(self.spath + "/" + "dl_log.json"):
                    os.remove(self.spath + "/" + "dl_log.json")
                    print(f" ** FYI : {self.spath}/dl_log has been removed - I'll make a new one as we progress **")
                    sys.exit()
        return         


    def get_channel_videos(self):

        """Get uploads playlist id""" 
        
        playlist_id = self.res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        next_page_token = None

        while True:
            self.res = youtube.playlistItems().list(playlistId=playlist_id, 
                                               part='snippet',
                                               maxResults=50,
                                               pageToken=next_page_token).execute()
          
            self.videos += self.res['items']
        
            next_page_token = self.res.get('nextPageToken')

            if next_page_token is None:
                break
            
        return self.videos


    def save_desc(self):
        """ Offer choice to save the Descriptions """
        desc_dic = {}
        
        resp_save_text = input("Do you want to save the descriptions? y/n ")
        if resp_save_text.lower() == "y":
            for idx, video in enumerate(self.videos):
                try:
                    print(video['snippet']['title'])
                    print(video['snippet']['description'])
                    print(video['snippet']['resourceId']['videoId']) 
                    
                    d_items = ([("id", video['snippet']['resourceId']['videoId']),
                                ("title", video['snippet']['title']),
                                ("description",video['snippet']['description'] + additional_text )])
                    
                    desc_dic[idx] = (d_items)
                except:
                    pass
    
            with open(self.full_path + "_desc.json", 'w') as json_file:
                json.dump(desc_dic, json_file)

                
    def save_videos(self):
        """ Offer choice to save the Videos - skip any that are marked as excluded-on-resume"""
        dl_completed = {}
        resp_save_text = input("Do you want to save the videos? y/n ")
        if resp_save_text.lower() == "y":
                for idx, video in enumerate(self.videos):
                    videoname = (video['snippet']['title'])
                    self.videodl = (video['snippet']['resourceId']['videoId'])
                    link = (f"http://youtube.com/watch?v={self.videodl}")
                    yt =YouTube(link)
                    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

                    try:
                            print(self.full_path + videoname +".mp4")                
                            if not os.path.isfile(self.full_path + videoname + ".mp4"):
                                print(self.full_path + videoname + " doesn\'t exist")                            
                                print(f"> Saving video {idx+1} {videoname}")
                                print('updating log file')
                                for i in tqdm(range(20)):
                                    stream.download(self.full_path)
                                    time.sleep(0.5)
                                dl_items = (self.videodl)   
                                dl_completed[idx+1] = (dl_items)

                            else:
                                print(f"The video : {videoname} already exisits so I'm skipping it")
                                
                    except:
                            print('Some error in downloading: ', link)
                            
                with open(self.spath + "/" + "dl_log.json", 'w') as json_file:
                            json.dump(dl_completed, json_file)
        return


    def resume_save_videos(self):
        """ check if there are any videos in dir already - check if json file created by a previous running of this script"""
        if os.path.exists(self.spath + "/" + "dl_log.json"):
            with open(self.spath + "/" + "dl_log.json") as f:
                data = json.loads(f.read())
            for i in data:             
                if data[i] not in self.videos:
                    self.exc_dl[i] = data[i]   
            self.save_videos()
        else:
            self.save_videos()
                

    def save_thumbs(self):
        """ Offer choice to save the thumbnails """
        resp_save_text = input("Do you want to save the thumbnails? y/n ")
        if resp_save_text.lower() == "y":
            for idx, image in enumerate(self.videos):

                                print(image['snippet']['thumbnails']['high']['url'])
                                url = (image['snippet']['thumbnails']['high']['url'])
                                s_name = url.split('/')[-2]
                                print(s_name)
                                totalvids = (len(self.videos))
                                print(f"Getting thumbnail number,{idx+1} of {totalvids}")
                                print("*" * idx)
                                r = requests.get(url, allow_redirects=True)

                                open(self.full_path + s_name +".jpg", 'wb').write(r.content)

            print (f"Done, now check you local directory /{self.spath}/{self.destd} for your thumbnails")


    def open_json(self):
        resp_save_text = input("Do you want to open the Descriptions - json) file)? y/n ")
        if resp_save_text.lower() == "y":
                with open(self.full_path + "_desc.json") as f:
                    data = json.loads(f.read())
                    print (json.dumps(data, indent = 4, sort_keys = True))

    def disp_desc(self):
        with open(self.full_path + "_desc.json") as f:
                    data = json.loads(f.read())
                    for i, val in data.items():
                        for key in val:
                            try:
                                print(key[1])
                                print("*"*40)
                            except:
                                pass


    def upload_new_desc(self):
        resp_save_text = input("Do you want to upload the NEW description? y/n ")
        if resp_save_text.lower() == "y":
            print("Get upload_video3.py from my GitHub page RGGH and follow the readme")


    def spacer(self):
        print("\n\n\n ")
                        
# MAIN #

if __name__ == "__main__":

        dls = Ytg()
        dls.md()
        dls.spacer()
        dls.list_dir()
        dls.spacer()
        dls.ask_destd() 
        dls.get_channel_videos()
        dls.spacer()
        dls.save_desc()
        dls.spacer()
        dls.resume_save_videos()
        dls.spacer()
        dls.save_thumbs()
        dls.spacer()
        dls.disp_desc()
        dls.spacer()
        dls.upload_new_desc()






