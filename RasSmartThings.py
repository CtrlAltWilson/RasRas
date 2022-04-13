#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import aiohttp
import asyncio
import pysmartthings

from tokens import SmartThings as SID

"""
api.devices()
    _api
    _device_id
    _name
    _label 
    _location_id
    _room_id
    _type
    _device_type_id
    _device_type_name
    _device_type_network
    _components
    _capabilities
    _status
    
api.scenes()
    _api
    _color
    _name
    _icon
    _location_id
    _scene_id

#i.e. Home
api.locations()	
    _api
    _name
    _location_id
    _latitude
    _longitude
    _region_radius
    _temperature_scale
    _locale
    _country_code
    _timezone_id

api.rooms()
api.apps()
api.installedapps()
api.subscriptions()
api.oauth()
	
"""


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = SID
#nest_asyncio.apply()

#working

def success():
    print("success!")

async def print_devices(item = None):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        counter = 1
        devicearray = []
        for device in devices:
            #print("{}: {}".format(device.device_id, device.label))
            #prints all devices
            try:
                if item.lower() in device.label.lower():
                    print("{}".format(device.label))
                    devicearray.append("{}\n".format(device.label))
            except:
                if item == None:
                    print("{}. {}".format(counter, device.label))
                    devicearray.append("{}. {}\n".format(counter,device.label))
                    counter += 1
        return "".join(devicearray)
            #List specific device from item
            #if item == device.label:
                #print("{}".format(device.label))

async def check_devices(item):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        counter = 1
        #this can be optimized
        #splits all devices names
        for device in devices:
            word_counter = 0
            #splits all words in device names
            for deSplit in device.label.lower().split():
                #splits all words from input
                for iteSplit in item.lower().split():
                    #ignores boring words to speed up the process
                    if 'turn' not in iteSplit or 'on' not in iteSplit or 'off' not in iteSplit:
                        if is_it_everything(item):
                            return 'everything'
                            break
                        elif (deSplit in iteSplit or iteSplit in deSplit):
                            word_counter += 1
                            if(len(device.label.split()) == word_counter):
                                return device.label
                                break
                        elif any(char.isdigit() for char in item) and is_it_num(item, counter):
                            return device.label
            counter += 1
        return 1

def is_it_num(item, counter):
    isNum = False
    for itSplit in item.split():
        if str(counter) == itSplit:
            isNum = True
            break
    return isNum
	
def is_it_everything(item):
    isEverything = False
    for itSplit in item.lower().split():
        if 'everything' == itSplit.lower() or 'all' == itSplit.lower():
            isEverything = True
            break
    return isEverything
     
async def print_scenes():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        scenes = await api.scenes()
        for scene in scenes:
            print("{}: {}".format(scene.device_id, scene.label))


async def print_locations():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        locations = await api.locations()
        for location in locations:
            #print("{}: {}".format(device.device_id, device.label))
            #prints all devices
            print("{}".format(location.__dict__))

async def set_device(item = None, state = None):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        for device in devices:
            if item == device.label or (item == 'everything' and 'light' in device.label.lower()):
                if 'ON' in state.upper():
                    try:
                        assert await device.switch_on() == True
                    except:
                        print("{} cannot turn on".format(device.label))
                        if 'light' in device.label.lower():
                            await device.command('main', 'light', "on")
                if 'OFF' in state.upper():
                    try:
                        assert await device.switch_off() == True
                    except:
                        print("{} cannot turn off".format(device.label))
                        if 'light' in device.label.lower():
                            await device.command('main', 'light', "off")

async def test():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        locations = await api.locations()
        for location in locations:
            #print("{}: {}".format(device.device_id, device.label))
            #prints all devices
            print("{}".format(location.__dict__))		


def RasRas_ST_Input(input):
    return asyncio.run(RasRas_main(input))

def RasRas_ST_getDevices():
    return asyncio.run(print_devices())


async def RasRas_main(input):
    set_item = await check_devices(input)
    for state in input.lower().split():
        if 'on' == state.lower() or 'off' == state.lower():
            await set_device(set_item, state)
            return ("Okay turning {} {}!".format(set_item,state))
        elif set_item == 1:
            return "No device found!"

async def main():
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(await print_devices())
    #loop.run_until_complete(test())
    #loop.close()
    await print_devices()
    #await test()
    #
    print()
    print("What do you want to do?") #todo check to see if item exists
    st_input = input()
    set_item = await check_devices(st_input)
    if 'exit' not in st_input.lower() and not set_item == 1:
            for state in st_input.lower().split():
                if 'on' == state.lower() or 'off' == state.lower():
                    await set_device(set_item, state)
                    print("Toggling {}".format(set_item))
                    success()
    elif set_item == 1:
        print("No device found!")
    else:
        print('Exiting')
    #print(await set_device())
    #await print_scenes()

"""
if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
"""