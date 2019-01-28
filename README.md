# README

spotify_lyrics_fetch is a python script that takes your Spotify username as input, fetches your currently playing song from Spotify and scrapes genius.com using BeautifulSoup to fetch the lyrics and print them to the terminal. This script uses the spotipy and bs4 libraries; as of Jan 10, 2019, pip install does not fetch the updated version of Spotipy, so it must be installed from github. The pip_install_dependencies shell script will install spotipy and bs4 with pip. 

Terminal usage:

bash pip_install_dependencies.sh
python spotify_lyrics_fetch.py USERNAME