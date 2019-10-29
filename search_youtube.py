'''
from apiclient.discovery import build

# Arguments needed for the build function
DEVELOPER_KEY = 'AIzaSyA6-f_nvbmJp6xTIRJfmR-dz7g0Q1mMVx8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Creating Youtube Resource Object
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

def youtube_search_keyword(query, max_results):

    # calling the search.list method to
    # retrieve youtube search results
    search_keyword = youtube_object.search().list(q = query, part = "id, snippet", maxResults = max_results).execute()
    
    # extracting the results from serach response
    results = search_keyword.get("items", [])
    
    # empty list to store video,
    # channel, playlist metadata
    videos = []
    channels = []
    playlists = []
    
    # extracting required info from each result object
    for result in results:
        # video result object
        if result['id']['kind'] == 'youtube# video':
            videos.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], 
                    result["id"]["videoId"], result['snippet']['description'], 
                    result['snippet']['thumbnails']['default']['url'])) 
                    
        # playlist result object
        elif result['id']['kind'] == 'youtube# playlist':
            playlists.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], 
                        result["id"]["playlistId"], 
                        result['snippet']['description'], 
                        result['snippet']['thumbnails']['default']['url'])) 
                         
         # channel result object
        elif result['id']['kind'] == 'youtube# channel':
            channels.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"], 
                       result["id"]["channelId"],  
                       result['snippet']['description'],  
                       result['snippet']['thumbnails']['default']['url'])) 
                       
    print("Videos:\n", "\n".join(videos), "\n") 
    print("Channels:\n", "\n".join(channels), "\n") 
    print("Playlists:\n", "\n".join(playlists), "\n") 
    
if __name__ == '__main__':
    youtube_search_keyword('Geeksforgeeks', max_results = 10)
'''

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ['https://www.googleapis.com/auth/youtube.readonly']

def main():
    # Disable OAuthLib HTTPS verification when running locally
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_703825584565-g67j6rqagbdfaj9ua8va5s0kf0k6krbf.apps.googleusercontent.com.json"
    
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    
    
    request = youtube.channels().list(
        part="id, snippet, contentDetails",
        id="UC57vbls4XfwhnloATzguCZQ"
    )
    response = request.execute()
    
    print(response)
    
if __name__ == '__main__':
    main()