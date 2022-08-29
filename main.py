import httpx
from base64 import b64encode, encode
#from dotenv import load_dotenv, find_dotenv  #testing
import os


#testing
#load_dotenv(find_dotenv())


REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN").strip()
CLIENT_ID = os.environ.get("CLIENT_ID").strip()
CLIENT_SECRET = os.environ.get("CLIENT_SECRET").strip()


def get_refresh_token():    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    r = httpx.post("https://accounts.spotify.com/api/token", data=data)

    try:
        r.raise_for_status()
        token = r.json()["access_token"]
        return token

    except httpx.HTTPStatusError as error:
        print(error)
        exit()


def get_user_info(access_token):
    url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": "Bearer " + access_token,
    }
    r = httpx.get(url, headers=headers)
    try:
        r.raise_for_status()
        return r.json()

    except httpx.HTTPStatusError as error:
        print(error)
        exit()


def get_recently_played_tracks(access_token):
    url = 'https://api.spotify.com/v1/me/player/recently-played'
    headers = {
        "Authorization": "Bearer " + access_token,
    }
    r = httpx.get(url, headers=headers)
    try:
        r.raise_for_status()
        return r.json()

    except httpx.HTTPStatusError as error:
        print(error)
        exit()



def main():
    token = get_refresh_token()
    userinfo = get_user_info(token)    
    tracks = get_recently_played_tracks(token) 
    tracks_played = []

    
    for track in tracks['items']:
        track_name = f"**{track['track']['name']}**"
        track_artists = [x['name']  for x in track['track']['artists']]
        track_album = track['track']['album']['name']
        full_track_info = f'{track_name} - {"|".join(track_artists)} Album: {track_album}'
        tracks_played.append(full_track_info)

    

    with open("README.md","w") as file:
        file.write("# github-actions-spotify-recent-tracks\n")
        file.write("muestro las ultimas canciones de mi cuenta spotify usando github actions\n")
        file.write("# Canciones:\n")
        file.write("\n")
        for track in tracks_played:
            file.write(f"- {track}\n")




if __name__ == "__main__":
    main()
