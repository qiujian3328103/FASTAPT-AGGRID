import pandas as pd 
import numpy as np 
from config import TEST_WAFER_MAP_SAMPLE_DATA
def create_wafer_data(root_lot_id):
    df_raw = pd.read_csv(TEST_WAFER_MAP_SAMPLE_DATA, index_col=False)
    
    # Filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001

    df['left'] = df['ucs_die_origin_x']*0.001 
    df['right'] = df['ucs_die_origin_x']*0.001
    df['bottom'] = df['ucs_die_origin_y'] *0.001
    df['top'] = df['ucs_die_origin_y']*0.001
    # Setting the width and height
    
    df["shot_bottom"] = df["ucs_die_y"]
    df["shot_left"] = df["ucs_die_x"]
    shot_width = 5
    shot_height = 12

    # Map the ucs_die_origin_x and ucs_die_origin_y to x and y, and set color
    df["color"] = "green"
    
    # Generate a list of dictionaries to match the format needed for D3.js
    single_wafer_data = df.apply(lambda row: {
        "x": row["left"],
        "y": row["bottom"],
        "color": row["color"],
        "bin_value": row["bin_value"],
        "mouseover": f"Die_X: {int(row['sort_die_x'])}\nDie_Y: {int(row['sort_die_y'])}"
    }, axis=1).tolist()
    
    # Generate a list of dictionaries to match the format needed for D3.js
    single_shot_data = df.apply(lambda row: {
        "x": row["shot_left"],
        "y": row["shot_bottom"],
        "color": row["color"],
    }, axis=1).tolist()
    
    wafer_data = {}
    for i in range(1, 26, 1):
        wafer_data.update({
            "{}-{}".format(root_lot_id, i) : single_wafer_data
        })
    
    shot_data = {}
    for i in range(1, 26, 1):
        shot_data.update({
            "{}-{}".format(root_lot_id, i) : single_shot_data
        })
        
    return wafer_data, shot_data, width, height