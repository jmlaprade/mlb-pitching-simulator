# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 14:32:56 2025

@author: Jeremy Laprade
"""

import pandas as pd
import os

def one_hot_encode(df, column_name, new_prefix):
    """
    One-hot encode a single column and rename the resulting columns with a prefix.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the column to encode.
    column_name : str
        The column to one-hot encode.
    new_prefix : str
        Prefix for the new one-hot encoded columns.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with one-hot encoded and renamed columns.
    """
    df = pd.get_dummies(df, columns=[column_name], drop_first=False)
    
    # Rename new columns
    rename_dict = {
        col: col.replace(f"{column_name}_", f"{new_prefix}")
        for col in df.columns if col.startswith(f"{column_name}_")
    }
    
    df.rename(columns=rename_dict, inplace=True)
    
    return df

def get_project_root(folder_name="scripts"):
    """
    Return the absolute path to the project root folder.
    
    Parameters
    ----------
    folder_name : str
        Name of the folder where the current script resides (default 'scripts').
        The project root is assumed to be its parent folder.
    
    Returns
    -------
    str
        Absolute path to the project root.
    """
    try:
        # Running as a script
        folder_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Running interactively (e.g., Spyder or Jupyter)
        folder_dir = os.getcwd()
    
    # Assume project root is parent folder of the script folder
    project_root = os.path.dirname(folder_dir)
    
    return project_root