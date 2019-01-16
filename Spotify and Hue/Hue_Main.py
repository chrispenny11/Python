#Chris Penny
#Documentation: https://developers.meethue.com/documentation/core-concepts
#Basic Hue Lights Control

import qhue
import serial
import time

def hue_basic(hue_count):
    # Connect to the bridge with a particular username
    from qhue import Bridge
    b = Bridge('192.168.0.24', 'COB9plogkaqukYuCoOvaO8hkI-ukMgzdL0BQp4MD')

    
    # This should give you something familiar from the API docs:
    print(b.url)

    lights = b.lights   # Creates a new Resource with its own URL
    print(lights.url)    # Should have '/lights' on the end

    # Get the bridge's configuration info as a dict,
    # and print the ethernet MAC address
    #print(b.config()['mac'])

    # Get information about light 1
    for i in range(5, 5):
        print(b('lights', i))


    #Attributes:
    # bri max = 254
    # sat max = 254
    # hue range = 0 to 65535
    #for j in range(1, 5):
    #    b.lights[j].state(on = True, bri=254, hue=10000)

    switch = 0

    while switch == 0:
        for j in range(1,6):
            b.lights[j].state(on = True, bri=254, sat = 254, hue=hue_count)
#            b.lights[j].state(on = True, bri=254, xy = get_artwork_colors())            
        time.sleep(100)

    while switch == 1:
        for j in range(1,6):
            b.lights[j].state(on = True, bri=254, sat = 254, hue=hue_count)
        time.sleep(100)

hue_basic(46920)

