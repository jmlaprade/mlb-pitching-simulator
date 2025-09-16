# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 15:37:02 2025

@author: Jeremy Laprade
"""

class Game:
    def __init__(self,pitcher,batter,balls=0,strikes=0,outs=0):
        self.pitcher = pitcher
        self.batter = batter
        self.inning = 1
        self.balls = balls
        self.strikes = strikes
        self.outs = outs
        self.score = 0

    def is_game_over(self):
        return self.outs >=3
        
    def display_state(self):
        state_string = f"Inning: {self.inning} | Balls: {self.balls} | Strikes: {self.strikes} | Outs: {self.outs} | Score: {self.score}"
        return print(state_string)
    
    def update_state(self, outcome):
        "Game state can update in the following ways:"
        "Ball, strike, hit, walk, or strikeout.  There are no fouls yet."
        "Input outcome: str format"
        if outcome == "strike":
            self.strikes += 1
            if self.strikes == 3:
                print("Strikeout!")
                self.strikes = 0
                self.balls = 0
                self.outs += 1
        if outcome == "ball":
            self.balls += 1
            if self.balls == 4:
                print("Batter walked!")
                self.balls = 0
                self.strikes = 0
        if outcome == "hit":
            self.balls = 0
            self.strikes = 0
        if outcome == None:
            print("Error: pitch returned with no outcome from batter!")