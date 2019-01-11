import sys
import os
import spotipy
import spotipy.util as util
import requests
from bs4 import BeautifulSoup
from rauth import OAuth2Service

def main():
    scope = 'user-read-currently-playing'

    #spotify_base_url = "https://api.spotify.com/v1/me/player/currently-playing"
    #spotify_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer BQAjRN59iBFegR54vzGYYGSq4n3o1rB9ZmoYpE-St0cjGhPkqOk-ky3HgitIxH-ZGrjhcseOlj4BCsWFafY2fGuig2885OXMalG663VRtejhx63MXcRED5XFDwIrVHAbTyhsAdOeqk8xhbaC'}

    username = sys.argv[1]
    token = util.prompt_for_user_token(username, scope, client_id='159802338ee54afeb479255460f53b55', client_secret='49529751774b459bb2684c780f4edeb3', redirect_uri='http://localhost/')
    if token:
        sp = spotipy.Spotify(auth=token)
        curr_track_json = sp.current_user_playing_track()
    curr_track_name = curr_track_json['item']['name']
    curr_track_artist_name = curr_track_json['item']['artists'][0]['name']
    print(curr_track_name)
    print(curr_track_artist_name)
    genius_base_url = "https://api.genius.com"
    genius_headers = {'Authorization': 'Bearer Xr9a6doEP7-EDGHveANf3_SqnwNnHce5stmizqwQbKSDWzUlm3L7MU_QjIQrwWck'}

    genius_search_url = genius_base_url + "/search"
    genius_data = {'q': str(curr_track_name + " " + curr_track_artist_name)}
    genius_response = requests.get(genius_search_url, data=genius_data, headers=genius_headers)
    genius_json = genius_response.json()
    song_info = None
    #print(genius_response)
    #print(genius_json)
    #print(genius_json["response"]["hits"])
    for hit in genius_json["response"]["hits"]:
        #print(hit)
        if hit["result"]["primary_artist"]["name"].find(curr_track_artist_name) != -1:
            #print("artist hit")
            song_info = hit
            break
    if song_info:
        #print("found")
        song_api_path = song_info["result"]["api_path"]
        #print(song_api_path)
        print(genius_lyrics_fetch(song_api_path, genius_base_url, genius_headers))

def genius_lyrics_fetch(api_path, genius_base_url, genius_headers):
    genius_song_url = genius_base_url + api_path
    genius_song_response = requests.get(genius_song_url, headers=genius_headers)
    genius_song_json = genius_song_response.json()
    path = genius_song_json["response"]["song"]["path"]
    #print(path)
    song_url = "https://genius.com" + path
    song_page = requests.get(song_url)
    #print(song_page)
    song_html = BeautifulSoup(song_page.text, "html.parser")
    [h.extract() for h in song_html('script')]
    lyrics = song_html.find("div", class_="lyrics").get_text()
    return lyrics

def test_genius():
    genius_base_url = "https://api.genius.com"
    genius_headers = {'Authorization': 'Bearer Xr9a6doEP7-EDGHveANf3_SqnwNnHce5stmizqwQbKSDWzUlm3L7MU_QjIQrwWck'}

    genius_search_url = genius_base_url + "/search"
    genius_data = {'q': "Waves"}
    genius_response = requests.get(genius_search_url, data=genius_data, headers=genius_headers)
    genius_json = genius_response.json()
    song_info = None
    print(genius_response)
    print(genius_json)
    print(genius_json["response"]["hits"])
    print("end test")
main()
