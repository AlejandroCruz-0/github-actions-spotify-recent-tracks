from textwrap import dedent


def tracks_markdown(track):
    markdown = f"""\n
    # **{track['track_name']}** {'|'.join(track['track_artists'])}

    ![Foto del album: {track['track_album']}]({track['album_image']})

    **Album:** {track['track_album']}

    📅 {track['played_at']}
    """

    return dedent(markdown)


def header_markdown(userinfo):
    markdown = f"""\n
        # github-actions-spotify-recent-tracks        

        muestro las ultimas canciones de mi cuenta spotify usando github actions

        # Info de mi Cuenta
        Nombre: **{userinfo['display_name']}**

        [Link perfil spotify]({userinfo['external_urls']['spotify']})

        # Canciones:
        
        """

    return dedent(markdown)
