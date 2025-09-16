# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 15:50:34 2025

@author: Jeremy Laprade
"""

class Pitcher:
    def __init__(self,name,stamina=1):
        self.name = name
        self.stamina = stamina
        self.pitch_types = ["fb"]
        
    def choose_pitch(self):
        pitch_type = input(f"Choose pitch type: {self.pitch_types}: ")
        location = input("Choose pitch location ['strike' or 'ball']: ")
        return {"type": pitch_type, "location": location}
