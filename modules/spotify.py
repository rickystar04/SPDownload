import json
import os
import urllib.request

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from . import cred
from .color import color

scope = "playlist-read-private"
try:
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=cred.client_ID,
            client_secret=cred.client_SECRET,
            redirect_uri=cred.redirect_url,
            scope=scope,
        )
    )

except spotipy.oauth2.SpotifyOauthError as e:
    print(f"{color.RED}Authentication error")


def run(playlist_id):
    playlist_URI = playlist_id.split("/")[-1].split("?")[0]

    playlist_name = sp.playlist(playlist_URI)
    results = sp.playlist_tracks(playlist_URI)

    tracks = results["items"]

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    i = 0

    playlist_name = playlist_name["name"]
    print(f"\nPlaylist: {color.CYAN}{playlist_name}{color.END}")

    json_data = {"$schema": "./tracks.schema.json", "Playlist": []}

    for track in tracks:
        i += 1
        print(
            f"{color.BLUE}[{i}]{color.END} {track['track']['name']} - {track['track']['artists'][0]['name']}"
        )
        track_name = track["track"]["name"]
        track_artist = track["track"]["artists"][0]["name"]
        track_album = track["track"]["album"]["name"]

        item = {
            "album": track_album,
            "artist": track_artist,
            "list": f"{track_name} - {track_artist}",
            "title": track_name,
        }

        json_data["Playlist"].append(item)

        image_link = track["track"]["album"]["images"][0]["url"]

    with open("tracks.json", "w") as f:
        json.dump(json_data, f)


def correct(playlist_id):
    playlist_URI = playlist_id.split("/")[-1].split("?")[0]

    playlist_name = sp.playlist(playlist_URI)
    results = sp.playlist_tracks(playlist_URI)

    tracks = results["items"]

    playlist_name = playlist_name["name"]

    if not os.path.exists("./music/" + playlist_name):
        os.mkdir("music/" + playlist_name)

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    i = 0
    for track in tracks:
        i += 1
        track_name = track["track"]["name"]
        image_link = track["track"]["album"]["images"][0]["url"]

        img = open(f"images/{track_name} cover.jpg", "wb")
        img.write(urllib.request.urlopen(image_link).read())
        img.close()
    return playlist_name
