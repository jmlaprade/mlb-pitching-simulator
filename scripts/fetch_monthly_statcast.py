# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 15:37:01 2025

@author: Jeremy Laprade
"""
from pybaseball import statcast
import os
from calendar import monthrange
import warnings
import pandas as pd
from utilities import get_project_root

warnings.simplefilter(action='ignore', category=FutureWarning)

allowed_pitch_types = ["4-Seam Fastball","Slider","Changeup","Curveball",
                       "Sinker","Cutter"]
data_subset = ["batter","description","pitch_name","release_speed",
               "release_spin_rate","plate_x","plate_z","stand",
               "p_throws","balls","strikes"]


project_root = get_project_root(folder_name="scripts")

# assemble output folder path
output_folder = os.path.join(project_root, "data", "raw")
os.makedirs(output_folder, exist_ok=True)

year = 2024

# data season is roughly 5 months long, with the starting month being april (=4)
for month in range(6):
    month = month+4
    month_str = f"{month:02d}"
    last_day = monthrange(year, month)[1]
    start_dt = f"{year}-{month_str}-01"
    end_dt = f"{year}-{month_str}-{last_day}"
    
    month_name = f"{year}_{month_str}"
    output_file = os.path.join(output_folder, f"{month_name}_raw.csv")
    
    fetch_data = False  # flag to decide whether to call statcast

    if os.path.exists(output_file):
        overwrite = input(f"{output_file} exists. Overwrite? [Y/N]: ").strip().lower()
        if overwrite == "y":
            fetch_data = True
        else:
            print(f"Skipping {month_name}, file already exists.")
            continue  # skip to next month

    else:
        # file does not exist → fetch normally
        fetch_data = True

    if fetch_data:
        print(f"Fetching Statcast data from {start_dt} to {end_dt}...")
        raw_data = statcast(start_dt=start_dt, end_dt=end_dt)

        if raw_data.empty:
            print(f"No data returned for {year}-{month_str}")
        else:
            # keep only requested subset + new features
            needed_cols = data_subset + ["launch_angle", "launch_speed", "at_bat_number"]
            clean_data = raw_data[needed_cols].copy()
        
            clean_data["pitch_name"] = clean_data["pitch_name"].str.strip()
            training_data = clean_data[clean_data["pitch_name"].isin(allowed_pitch_types)].copy()
        
            # handle NaNs in launch features and at_bat_number
            training_data['launch_angle'] = training_data['launch_angle'].fillna(-1)
            training_data['launch_speed'] = training_data['launch_speed'].fillna(-1)
        
            # convert at_bat_number to lineup spot (1–9, -1 for unknowns)
            def at_bat_to_lineup(at_bat):
                if at_bat <= 0:
                    return -1
                spot = int(at_bat) % 9
                return 9 if spot == 0 else spot
        
            training_data['lineup_spot'] = training_data['at_bat_number'].apply(at_bat_to_lineup)
            
            # drop at_bat_number (we only keep lineup_spot)
            training_data = training_data.drop(columns=["at_bat_number"])
            # save CSV with all features
            training_data.to_csv(output_file, index=False)
            print(f"Saved {output_file}, rows: {len(training_data)}")
