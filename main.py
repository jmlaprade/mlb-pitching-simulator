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
        if game.strikes == 0 and game.balls == 0:
            # player needs an update to game state upon new batter
            game.display_game_state()
            game.display_runner_state()
            # player needs an update to count on each pitch, except for first
        else:
            game.display_count()
            
        pitch = pitcher.choose_pitch()
        outcome = batter.determine_outcome(pitch)
        print(f"Pitch outcome: {outcome}")
        game.update_state(outcome)
        
    print("Game over!")
        
if __name__ == "__main__":

    main()
