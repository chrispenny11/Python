import sys
import spotipy
import spotipy.util as util

scope = 'user-read-currently-playing'

token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='https://developer.spotify.com/dashboard/applications/dd41386aabca41aa8dd7ba2f947782b3')

print(token)

spotifyObject = spotipy.Spotify(auth=token)


track = spotifyObject.current_user_playing_track()

##sp = spotipy.Spotify(auth=token)
##
##results = sp.user_playlists("Chris Penny")
##for item in results['items']:
##    track = item['track']
##    print(track['name'] + ' - ' + track['artists'][0]['name'])
##
##
##birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
##spotify = spotipy.Spotify()
##
##results = spotify.artist_albums(birdy_uri, album_type='album')
##albums = results['items']
##while results['next']:
##    results = spotify.next(results)
##    albums.extend(results['items'])
##
##for album in albums:
##    print(album['name'])
##
##import spotipy
##sp = spotipy.Spotify()
##
##results = sp.search(q='weezer', limit=20)
##for i, t in enumerate(results['tracks']['items']):
##    print(' ', i, t['name'])
