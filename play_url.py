# Inspiration code: https://stackoverflow.com/questions/28440708/python-vlc-binding-playing-a-playlist/33042754
# Inspiration code: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests

import pafy
import vlc
import requests
from time import sleep
import search_youtube as sy

results = sy.youtube_search_keyword("Admiralbulldog", 10)
video_urls = []
for item in results:
    yt_link = 'https://www.youtube.com/watch?v=' + item['video_id']
    video = pafy.new(yt_link)
    bestaudio = video.getbestaudio()
    play_url = bestaudio.url
    video_urls.append(play_url)

playlists = set(['pls','m3u'])

Instance = vlc.Instance()

for url in video_urls:
    ext = (url.rpartition(".")[2])[:3]
    test_pass = False
    try:
        if url[:4] == 'file':
            test_pass = True
        else:
            r = requests.get(url, stream=True)
            test_pass = r.ok
    except Exception as e:
        print('failed to get stream: {e}'.format(e=e))
        test_pass = False
    else:
        if test_pass:
            print('Sampling for 15 seconds')
            player = Instance.media_player_new()
            Media = Instance.media_new(url)
            Media_list = Instance.media_list_new([url])
            Media.get_mrl()
            player.set_media(Media)
            if ext in playlists:
                list_player = Instance.media_list_player_new()
                list_player.set_media_list(Media_list)
                if list_player.play() == -1:
                    print ("Error playing playlist")
            else:
                if player.play() == -1:
                    print ("Error playing Stream")
            sleep(15)
            if ext in playlists:
                list_player.stop()
            else:
                player.stop()

        else:
            print('error getting the audio')
