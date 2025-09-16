# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 15:43:40 2025

@author: Jeremy Laprade
"""

from src.game import Game
from src.pitcher import Pitcher
from src.batter import Batter

def main():
    pitcher = Pitcher("Username")
    batter = Batter("AIBatter")
    game = Game(pitcher,batter)
    
    while not game.is_game_over():
        game.display_state()
        pitch = pitcher.choose_pitch()
        outcome = batter.determine_outcome(pitch)
        print(f"Pitch outcome: {outcome}")
        game.update_state(outcome)
        
    print("Game over!")
        
if __name__ == "__main__":
    main()