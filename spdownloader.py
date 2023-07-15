import json
import os
import re
import urllib.request

import yt_dlp

from modules import spotify
from modules.banner import banner
from modules.color import color
from modules.metadata import image

# try:
os.system("cls" if os.name == "nt" else "clear")
banner(0.03)

if not os.path.exists("music"):
    os.mkdir("music")

if not os.path.exists("images"):
    os.mkdir("images")

while True:
    playlist_id = input("Paste playlist link: ")

    spotify.run(playlist_id)

    if input("Is this the right playlist?? [y/n] >>> ") == "y":
        playlist_name = spotify.correct(playlist_id)
        break
    else:
        os.system("cls" if os.name == "nt" else "clear")
        banner(0)

i = 0

with open("tracks.json", "r") as file:
    data = json.load(file)
    data_length = len(data["Playlist"]) + 1

for line in data["Playlist"]:
    i += 1

    query = urllib.parse.quote(line["list"] + " lyrics")

    url = "https://www.youtube.com/results?search_query=" + query

    html = urllib.request.urlopen(url)

    link = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    url = f"https://www.youtube.com/watch?v={link[0]}"

    title = line["title"]
    artist = line["artist"]
    album = line["album"]

    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "outtmpl": f"/music/{playlist_name}/{title}.%(ext)s",
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
    image(title, artist, album, playlist_name)

    print(
        f"{color.GREEN}[✓ {i}/{data_length}]{color.BOLD}{title}{color.END}{color.GREEN} successfully downloaded\033[0m"
    )
# except Exception as err:
# print(err)
# print(f"{color.RED} SOMETHING HAS GONE WRONG TRY AGAIN LATER...")

# finally:
# os.remove("tracks.json")

dir = "images/"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

print(color.BOLD + color.PURPLE + "\nFinished!" + color.END)
