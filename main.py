import requests
from pprint import PrettyPrinter
import spotipy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET =os.getenv("CLIENT_SECRET")
REDIRECT_URL = "http://example.com"
TEST_SONG = "One Dance"
pp = PrettyPrinter(indent=4)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope="playlist-modify-private",
        cache_path=".cache")
                     )

user_id = sp.current_user()["id"]
# print(user_id)

################################# 100 songs below #######################################

date_entry = input('Enter a date in YYYY-MM-DD format: ')
# date_entry = "2002-07-20"
web_url = f"https://www.billboard.com/charts/hot-100/{date_entry}"

response = requests.get(web_url)
website = response.text

soup = BeautifulSoup(website, "html.parser")

all_song_tags = soup.find_all(name="span", class_="chart-element__information__song")
song_titles = [songs.getText() for songs in all_song_tags]
# print(song_titles)

tracks = []

for song in song_titles:
    track_data = sp.search(q=f"track: {song}", type="track", limit=1)
    try:
        track_url = track_data["tracks"]["items"][0]["external_urls"]["spotify"]
        tracks.append(track_url)
    except IndexError as error_message:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# pp.pprint(tracks)

######################################## Create playlist #############################################

# new_playlist = sp.user_playlist_create(user=user_id, name=f"{date_entry} Billboard 100", public=False)
# print(new_playlist)
billboard_playlist_id = "spotify:playlist:0lkTivkex6ifZ525qz6yHQ"

sp.playlist_add_items(playlist_id=billboard_playlist_id, items=tracks)
# pp.pprint(sp.playlist_items(playlist_id=billboard_playlist_id))


################## for auto find playlist #########################
# playlists = sp.user_playlists(user=user_id, limit=10)
# pp.pprint(playlists['items'][0]["name"])
#

# #Creating a new private playlist in Spotify
# playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
#
# #Adding songs found into the new playlist
# sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)