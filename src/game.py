# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 15:37:02 2025

@author: Jeremy Laprade
"""

class Game:
    def __init__(self,pitcher,batter,balls=0,strikes=0,outs=0,):
        self.pitcher = pitcher
        self.batter = batter
        self.inning = 1
        self.balls = balls
        self.strikes = strikes
        self.outs = outs
        self.score = 0
        self.bases = {"first":False, "second":False, "third":False}
        
    def is_game_over(self):
        return self.outs >=3
        
    def display_game_state(self):
        return print(f"IN: {self.inning} | O: {self.outs} | Score: {self.score}")
    
    def display_count(self):
        return print(f"B:{self.balls} | S: {self.strikes}")
    
    def display_runner_state(self):
        occupied_bases = []
        for base, occupied in self.bases.items():
            if occupied:
                occupied_bases.append(base)
        if len(occupied_bases) == 3:
            return print("Bases loaded!")    
        elif len(occupied_bases) == 2:
            return print(f"Runners on {occupied_bases[0]} and {occupied_bases[1]}.")
        elif len(occupied_bases) == 1:
            return print(f"Runner on {occupied_bases[0]}.")
        else:
            return print("Bases empty.")
        
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
            
            # four balls walks a batter and resets the count
            if self.balls == 4:
                print("Batter walked!")
                self.balls = 0
                self.strikes = 0
                
                # if forced, the runner on third leaves and scores
                if self.bases["third"] and self.bases["second"] and self.bases["first"]:
                    self.bases["third"] = False
                    self.score += 1
                    
                # if forced, the runner on second leaves for third
                if self.bases["second"] and self.bases["first"]:
                    self.bases["third"] = True
                    self.bases["second"] = False
                    
                 # if forced, the runner on first leaves for second
                if self.bases["first"]:
                    self.bases["second"] = True  
                    self.bases["first"] = True
                    
                # batter becomes a runner on first
                self.bases["first"] = True
                
        # advance runners and reset count on hit
        if outcome == "hit":
            self.balls = 0
            self.strikes = 0
            # score runner from third base
            if self.bases["third"]:
                self.score += 1
                self.bases["third"] = False
            # advance runner to third from second
            if self.bases["second"]:
                self.bases["second"] = False
                self.bases["third"] = True
            # advance runner to second from first
            if self.bases["first"]:
                self.bases["first"] = False
                self.bases["second"] = True
            self.bases["first"] = True
            
        if outcome == None:
            print("Error: pitch returned with no outcome from batter!")
            
        
