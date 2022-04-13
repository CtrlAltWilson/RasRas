#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.


import logging
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def resp_nothing_is_playing():
    responses = [
        "Hey! There's nothing playing right now!",
        "You gotta play a song for me to see it!",
        "Nothing's playing!"
    ]
    resp_choice = random.choice(responses)
    return resp_choice

def resp_now_playing():
    responses = [
        "You got it! Now playing "
    ]
    resp_choice = random.choice(responses)
    return resp_choice

def resp_already_playing():
    responses = [
        "Something is already playing!"
    ]
    resp_choice = random.choice(responses)
    return resp_choice