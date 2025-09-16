# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 16:18:27 2025

@author: Jeremy Laprade
"""

import random

class Batter:
    def __init__(self,name):
        self.name = name
        
    def decide_swing(self, pitch):
        "Cause the batter to decide whether to swing, based on pitch location"
        # batter is more likely to swing at strikes than balls
        if pitch["location"].strip().lower()  == "strike":
            swing_probability = 0.7
        else:
            swing_probability = 0.2
        return random.random() < swing_probability
    
    def determine_outcome(self, pitch):
        swing = self.decide_swing(pitch)
        if swing:
            #strikes are easier to hit
            if pitch["location"].strip().lower()  == "strike":
                if random.random() < 0.1:
                    return "hit"
                else:
                    return "strike" 
            # balls are harder to hit
            if pitch["location"].strip().lower()  == "ball":
                if random.random() < 0.01:
                    return "hit"
                else:
                    return "strike"
        else: 
            return pitch["location"]