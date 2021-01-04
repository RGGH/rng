from pytube.cli import on_progress
from pytube import YouTube

video_url = "https://youtu.be/1GmOeQO6yOU"

def yt_dl(url):

	try:
	    yt = YouTube(url, on_progress_callback=on_progress)
	    yt.streams\
	        .filter(progressive=True, file_extension='mp4')\
	        .get_highest_resolution()\
	        .download()
	    
	except EOFError as err:
	    print(err)

	else:
	    print("\n====== Done - Check Download Dir =======")

# main driver #
if __name__ == '__main__':
	yt_dl(video_url)

