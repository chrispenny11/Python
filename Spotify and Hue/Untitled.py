
import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import urllib.request as req

def get_artwork_colors():
    # Get the username from terminal
    #username = sys.argv[1]
    scope = 'current_user_playing_track user-read-private user-read-playback-state user-modify-playback-state'

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')
    #    token = util.prompt_for_user_token(username, scope) # add scope
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
    #    token = util.prompt_for_user_token(username, scope) # add scope
        token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')

    # Create our spotify object with permissions
    sp = spotipy.Spotify(auth=token)

    # Get current device
    #devices = spotifyObject.devices()
    #deviceID = devices['devices'][0]['id']

    ##### Current track information
    ##track = spotifyObject.current_user_playing_track()
    ##artist = track['item']['artists'][0]['name']
    ##track = track['item']['name']
    ##
    ##if artist != "":
    ##    print("Currently playing " + artist + " - " + track)

    # User information
    user = sp.current_user()
    displayName = user['display_name']
    followers = user['followers']['total']
    #print(user)
    #print(dir(user))

    #result = sp.search('Mogwai')
    #print(result)

    track = sp.current_user_playing_track()
    #print(list(track))
    items = track['item']
    string_items = str(items)
    image_loc = string_items.find('images')
    image_loc_end = string_items.find('width', image_loc)
    image_url = string_items[image_loc+34:image_loc_end-4]
    req.urlretrieve(image_url, "Temporary Image Directory/temp_artwork.jpg")
    #print(test_item)
    #print(dir(track))
    #image_url = track['is playing']
    #print(image_url)

    from PIL import Image, ImageFilter
    try:
        album_art = Image.open("Temporary Image Directory/temp_artwork.jpg")
    except:
        print("Unable to load image")

    histogram = album_art.histogram()
    r_hist = histogram[1:256]
    r_hist = r_hist.index(max(r_hist))
    g_hist = histogram[257:512]
    g_hist = g_hist.index(max(g_hist))
    b_hist = histogram[513:768]
    b_hist = b_hist.index(max(b_hist))

    import numpy as np
    import colour

    # Assuming sRGB encoded colour values.
    RGB = np.array([r_hist, g_hist, b_hist])

    # Conversion to tristimulus values.
    XYZ = colour.sRGB_to_XYZ(RGB / 256)

    # Conversion to chromaticity coordinates.
    xy = colour.XYZ_to_xy(XYZ)
    print(xy)
    return(xy)

    # Conversion to correlated colour temperature in K.
    ##CCT = colour.temperature.xy_to_CCT_Hernandez1999(xy)
    ##print(CCT)

get_artwork_colors()
