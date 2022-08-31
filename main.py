import httpx
from dotenv import load_dotenv, find_dotenv  # testing
import os
from datetime import datetime
import pytz
import logging
import logging.handlers

# testing
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


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
        logger.error(error)
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
        logger.error(error)
        exit()


def get_recently_played_tracks(access_token):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        "Authorization": "Bearer " + access_token,
    }
    r = httpx.get(url, headers=headers)
    try:
        r.raise_for_status()
        return r.json()

    except httpx.HTTPStatusError as error:
        print(error)
        logger.error(error)
        exit()


def get_chilean_time(time):
    # Función para convertir el tiempo UTC sin offset de la propiedad played_at
    # De la respuesta de la api de Spotify, a tiempo Chileno

    try:
        # Mejorar esto
        year = int(time[:4])
        month = int(time[5:7])
        day = int(time[8:10])
        hour = int(time[11:13])
        minute = int(time[14:16])
        second = int(time[17:19])

        # Crear nueva datetime con tiempo utc
        my_datetime = datetime(year, month, day, hour, minute, second, tzinfo=pytz.utc)
        # convertir a tiempo chileno
        my_chile_time = my_datetime.astimezone(
            pytz.timezone("America/Santiago")
        ).strftime("%Y-%m-%d %H:%M:%S")
        return my_chile_time
    except Exception as error:
        logger.error(error)
        exit


def main():
    token = get_refresh_token()
    userinfo = get_user_info(token)
    tracks = get_recently_played_tracks(token)
    tracks_played = {}

    for id, track in enumerate(tracks["items"]):
        track_name = track["track"]["name"]
        track_artists = [x["name"] for x in track["track"]["artists"]]
        track_album = track["track"]["album"]["name"]
        played_at = get_chilean_time(track["played_at"])
        album_image = track["track"]["album"]["images"][1]["url"]  # tamaño 300
        tracks_played[id] = {
            "track_name": track_name,
            "track_artists": track_artists,
            "track_album": track_album,
            "played_at": played_at,
            "album_image": album_image,
        }

    with open("README.md", "w") as file:
        file.write("# github-actions-spotify-recent-tracks\n")
        file.write(
            "muestro las ultimas canciones de mi cuenta spotify usando github actions\n"
        )
        file.write("# Info de mi Cuenta\n")
        file.write(f"Nombre: **{userinfo['display_name']}**\n")
        file.write(f"[Link perfil spotify]({userinfo['external_urls']['spotify']})\n")
        file.write("")
        file.write("# Canciones:\n")
        file.write("\n")
        for id, track in tracks_played.items():
            # file.write(" Canción:\n")
            file.write(f"# {track['track_name']}-{'|'.join(track['track_artists'])}\n")
            # file.write(f"{'|'.join(track['track_artists'])}\n")
            file.write(
                f"![Foto del album: {track['track_album']}]({track['album_image']})"
            )
            file.write("\n")
            file.write(f"## Album: {track['track_album']}\n")
            file.write(f"### Tiempo de reproducción: {track['played_at']}\n")
            file.write("\n")

    logger.info("Operación completada")


if __name__ == "__main__":
    main()
