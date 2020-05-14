# Extract comments youtube.comments.list per video
# Run with API Key in separate file
# Source from : 
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from pprint import pprint
import googleapiclient.discovery
import json
from API_Key import myapi

# Parse the response from the API request
def parse(response):
    print("response =")
    #print("Length : %d" % len(response))
    dlen = len(response)
    num_comments = dlen-1
    print(f"Number of Comments =", num_comments)
    
    for i in range(0,num_comments):    
       
        comments = (response['kind'])
        text = (response['etag'])
        replies = (response['items'])
        replies = (replies[i]
            ['snippet']['topLevelComment'] \
            ['snippet']['textOriginal'])
        print("-"*10)
        #print(f"Comment= ",comments)
        #print(f"Text=", text)
        print(f"\t>>Comment:>>\n", replies)
         
    top_comment = (response['items'])
    top_comment = (top_comment[0]['snippet']['topLevelComment'] \
                                 ['snippet']['textDisplay'])
    print(f"\n****top comment**** =", top_comment)
    print("\nThe end!")
    print("\n")
    
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = myapi

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId="MamR5L2w03Q"
    )
    
    response = request.execute()

    # Extract the comments/replies and print to screen
    parse(response)
               

# main driver
if __name__ == "__main__":
    main()
