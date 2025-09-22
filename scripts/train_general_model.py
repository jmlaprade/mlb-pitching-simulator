# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 10:28:02 2025

@author: Jeremy Laprade
"""

import pandas as pd
import glob
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from utilities import one_hot_encode, get_project_root

# =========================
# CONFIG
# =========================
model_file_name = "generic_RF_swing.pkl"

project_root = get_project_root()
csv_folder = os.path.join(project_root, "data", "raw")
model_output = os.path.join(project_root, "data", "models", model_file_name)

drop_columns = ['description', 'launch_speed','launch_angle','batter']
swing_events = ["swinging_strike", "foul", "foul_tip", "hit_into_play"]
target_column = 'swing'

# =========================
# LOAD AND COMBINE DATA
# =========================
csv_files = sorted(glob.glob(f"{csv_folder}/*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {csv_folder}")

data_list = []
print("Loading data...")
for file in csv_files:
    df = pd.read_csv(file)

    # One-hot encode pitch types
    df = one_hot_encode(df, column_name='pitch_name', new_prefix='')

    # Convert events to binary swing target
    df['swing'] = df['description'].isin(swing_events).astype(int)
    
    # Encode batter handedness
    df = one_hot_encode(df, column_name='stand', new_prefix='batter_side_')
    
    # Encode pitcher handedness
    df = one_hot_encode(df, column_name='p_throws', new_prefix='pitcher_side_')
    
    # Drop irrelevant columns
    df = df.drop(columns=drop_columns)
    data_list.append(df)
    
# Combine all CSVs
full_data = pd.concat(data_list, ignore_index=True)
print(f"Data loaded. Total rows after combining: {len(full_data)}")

# =========================
# PREPARE FEATURE LIST
# =========================
X = full_data.drop(columns=[target_column])
y = full_data[target_column]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN RANDOM FOREST
# =========================
rf = RandomForestClassifier(
    n_estimators=200, max_depth=15, n_jobs=-1, random_state=42
)
print("Training Random Forest...")
rf.fit(X_train, y_train)
print("Training complete.")

# =========================
# EVALUATE
# =========================
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))

# =========================
# SAVE MODEL
# =========================
joblib.dump(rf, model_output)
print(f"Trained model saved to {model_output}")