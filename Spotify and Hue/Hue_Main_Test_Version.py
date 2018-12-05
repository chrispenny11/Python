#Chris Penny, 2/10/17
#Documentation: https://developers.meethue.com/documentation/core-concepts
#Basic Hue Lights Control

import qhue
import time
import Color_Extraction_Main

def hue_basic():
    # Connect to the bridge with a particular username
    xy = Color_Extraction_Main.get_artwork_colors()
    print(xy[1])
    
    from qhue import Bridge
    bridge_obj = Bridge('192.168.0.28', '3GDMt591RrPH6lsLfe2MkE0HRAkrhzzXAP1kGSOy')

    lights = bridge_obj.lights   # Creates a new Resource with its own URL

#    for i in range(1, 7):
#        print('iteration')
#        print(i)
#        print(bridge_obj('lights', i))

    bridge_obj.lights[5].state(on = True, bri=175, xy = xy[0])
    bridge_obj.lights[6].state(on = True, bri=175, xy = xy[1])
    bridge_obj.lights[4].state(on = True, bri=175, xy = xy[0])

#    bridge_obj.lights[4].state(on = True, bri=254, xy = [0.45188347, 0.47210205])
#    bridge_obj.lights[5].state(on = True, bri=254, xy = [ 0.3350179, 0.57124529])

#    time.sleep(100)
