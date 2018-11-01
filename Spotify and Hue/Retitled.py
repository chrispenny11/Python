# Initialize
import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError as JSONDE
import urllib.request as req
import numpy as np

# Define function for obtaining colors to pass to Philips Hue API Wrapper (phue package)
def get_artwork_colors():
    
    # Define scope
    scope = 'current_user_playing_track user-read-private user-read-playback-state user-modify-playback-state'

    # Obtain Spotify Token (username, client_id, and client_secret will vary per user - for additional information see Spotify API documentation.)
    try:
        token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')
    # Error Case - Remove token cache and replace
    except (AttributeError, JSONDE):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')

    # Generate spotipy object using Spotify Token
    spot_obj = spotipy.Spotify(auth=token)

    # Call spotipy attribute for the currently playing track
    track = spot_obj.current_user_playing_track()
    #print(list(track)) # For Debug

    # NOTE: While the current_user_playing_track() attribute results in a dictionary, the album art image URL is not assigned to a key and must be extracted by parsing.
    items = track['item']
    
    # Convert dictionary object to string and parse the album art image URL.
    string_items = str(items)
    image_loc = string_items.find('images')
    image_loc_end = string_items.find('width', image_loc)
    image_url = string_items[image_loc+34:image_loc_end-4]

    # Use the urllib library to save the image as a temporary file in a sub-directory.
    req.urlretrieve(image_url, "Temporary Image Directory/temp_artwork.jpg")
    #print(image_url) # For Debug

    from PIL import Image, ImageFilter
#    try:
    album_art_test = Image.open("Temporary Image Directory/temp_artwork.jpg").convert("L")
    album_art = Image.open("Temporary Image Directory/temp_artwork.jpg")
    print(album_art.mode)
    print(album_art)
    r, g, b = album_art.split()
    print(album_art.split())
#    album_art_single = album_art.merge("RGB", (b, g, r))#
#    print([r, g, b])
        
#    except:
#        print("Unable to load image")

    histogram = album_art.histogram()
    rgb_data = album_art.load()
    print(rgb_data)

#Test
    width, height = album_art.size

    all_pixels = []
    for i in range(width):
        for j in range(height):
            rgb_pixel = rgb_data[i, j]
            all_pixels.append(rgb_pixel)
    print(all_pixels)
    
    histogram_test = album_art_test.histogram()
    print(histogram_test)
    r_hist = histogram[1:256]
    r_hist_max = r_hist.index(max(r_hist))
#    r_hist_max = r_hist.index(max(r_hist[r_hist < round(.85*r_hist_max)]))
#    r_hist_select = [num for num in r_hist if r_hist >  and num % 7 == 0]
    g_hist = histogram[257:512]
    g_hist_max = g_hist.index(max(g_hist))
    b_hist = histogram[513:768]
    b_hist_max = b_hist.index(max(b_hist))
    rgb_max = [r_hist_max, g_hist_max, b_hist_max]
    print(rgb_max)

    import matplotlib
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    fig, test = plt.subplots()
    ax.plot(r_hist, 'r')
    ax.plot(g_hist, 'g')
    ax.plot(b_hist, 'b')
    ax.plot(histogram_test, 'black')
    plt.show()

    import numpy as np
    import colour

    # Assuming sRGB encoded colour values.
    RGB = np.array([r_hist_max, g_hist_max, b_hist_max])

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
