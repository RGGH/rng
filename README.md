# Red And Green - YouTube API download / upload repo

<b><p><center>![Red And Green Code](https://github.com/RGGH/rng/blob/master/redandgreenlogo.png)
</center></p></b>
<b>YouTube Channel Video, Description, and Thumbnail Downloader : (Linux Version)</b>
<b>ytapithumbget.py</b>

<b>YouTube Channel Video Description Uploader : (Linux Version)</b>
<b>upload_video3.py</b>

To use this you will have to make your own file called apikey.py and put it in the same directory as ytapithumbget.py

The format needs to be 

api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 

where the xxxx is YOUR YouTube API key that you get from them....
It needs to be in quotes too, as it is a string in Python.

To run, just type the following from your terminal shell:

<b>python3 ytapithumbget.py<b>
  
It will prompt you for a folder name to store the saved images in - this folder will be created inside a 'youtube_downloads' folder in your installation directory.

Next : run update_video3.py, make sure you have the right "_desc.json" file in the directory where you run these scripts from.
You can find the correct file for this in the folder that you made when you ran "ytapithumbget.py"

Watch the video guide to set up the API and run the code on our 'RedAndGreen YouTube channel' : https://www.youtube.com/watch?v=8h17wxgqNXY

Any issues contact me via the contact page at www.redandgreen.co.uk
