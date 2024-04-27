from fastapi import FastAPI, Request, Form, APIRouter, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import pandas as pd 
from app.library.helper import openfile
from sqlalchemy.orm import Session
from typing import List
from app.library.database import get_db
from app.library.models import SWLY_LABEL_DATA
from app.library.helper import CustomJinja2Templates


router = APIRouter()
templates = CustomJinja2Templates(directory="templates/")


def aggreate_to_dict(series):
    """
     series data as dictionary 
    Args:
        series (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {BIN_ITEM: BIN_VALUE for BIN_ITEM, BIN_VALUE in series}

# @router.get("/detail_page")
# async def detail_page(lot_id: str = Query(...), wafer_id: str = Query(...)):
#     # Process the selected row data
#     return {"lot_id": lot_id, "wafer_id": wafer_id}

@router.get("/detail_page", response_class=HTMLResponse)
async def detail_page(request: Request, lot_id: str = Query(...), wafer_id: str = Query(...)):
    print(lot_id, wafer_id)
    # Create a sample Bokeh plot
    # p = figure(plot_width=400, plot_height=400)
    # p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20)

    # Generate Bokeh components
    # script, div = components(p)
    # return templates.TemplateResponse("waferlabel.html", {"request": request, "lot_id": lot_id, "wafer_id": wafer_id, "plot_script": script, "plot_div": div})
    # df_raw = pd.read_csv(r"C:\Users\Jian Qiu\Dropbox\pythonprojects\django_web1\sample.csv", index_col=False)
    df_raw = pd.read_csv(r"/Users/JianQiu/Dropbox/pythonprojects/django_web1/sample.csv", index_col=False)
    
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
    wafer_data = df.apply(lambda row: {
        "x": row["left"],
        "y": row["bottom"],
        "color": row["color"],
        "bin_value": row["bin_value"],
        "mouseover": f"Die_X: {int(row['sort_die_x'])}\nDie_Y: {int(row['sort_die_y'])}"
    }, axis=1).tolist()
    
        # Generate a list of dictionaries to match the format needed for D3.js
    shot_data = df.apply(lambda row: {
        "x": row["shot_left"],
        "y": row["shot_bottom"],
        "color": row["color"],
    }, axis=1).tolist()
    
    # markdown to show the dieloss rule 
    markdown_data = openfile("home.md")
    
    # set default preocess_id 
    process_id = "UXPZ"
    
    # set default wafer_ids
    wafer_ids = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]
    selected_wafer_ids = ["01", "02", "03"]
    
    # set default swly_labels
    swly_labels = ["CMP Arc Scartch", "Over Polish", "Focus Spot", "TS Unlanded", "PC-TS UnderShort", "PC Footing"]
    
    # setup swly_bins
    swly_bins = ["BIN1001", "BIN1002", "BIN1003", "BIN1004", "BIN1019", "BIN1018", "BIN1017", "BIN1016"]
    
    # read the bindata.csv and render the data to html page 
    df_bins = pd.read_csv(r"/Users/JianQiu/Dropbox/pythonprojects/fastapi-aggrid/tests/bindata.csv", index_col=False)
    df_bins["WAFER_ID"] = df_bins["WAFER_ID"].astype(str).str.zfill(2)
    print(df_bins)
    summary = df_bins.groupby('BIN_ITEM')['BIN_VALUE'].sum().reset_index()
    top_items = summary.sort_values(by='BIN_VALUE', ascending=False).head(10)
    top_failure = top_items.to_dict(orient="records")
    
    summaryzied_by_waferID = df_bins.groupby("WAFER_ID").apply(lambda x: aggreate_to_dict(zip(x["BIN_ITEM"], x["BIN_VALUE"]))).reset_index()
    # rename 
    summaryzied_by_waferID.columns = ["WAFER_ID", "Data"]
#   returned data formate for summaryzied_by_wafer_ID                     
#         1  {'BIN1001': 0.2, 'BIN1002': 3.0, 'BIN1003': 4....
#         2  {'BIN1001': 0.2, 'BIN1002': 2.0, 'BIN1003': 2....
    summaryzied_by_waferID_json = summaryzied_by_waferID.to_json(orient="records")
    print(summaryzied_by_waferID_json)
    return templates.TemplateResponse("waferlabel.html", {"request": request, 
                                                          "lot_id": lot_id, 
                                                          "wafer_ids": wafer_ids, 
                                                          "markdown_data": markdown_data,
                                                          "waferData": wafer_data,
                                                          "shotData": shot_data,
                                                          "rectWidth": width,
                                                          "rectHeight": height, 
                                                          "shotWidth":shot_width,
                                                          "shotHeight":shot_height,
                                                          "process_id": process_id, 
                                                          "selected_wafer_ids":selected_wafer_ids, 
                                                          "swly_labels":swly_labels, 
                                                          "swly_bins":swly_bins,
                                                          "top_bin_items": top_failure,
                                                          "summaryzied_by_waferID": summaryzied_by_waferID_json,
                                                          })


@router.post("/submit_swly_label_data", response_class=HTMLResponse)
async def submit_swly_label_data(request: Request, wafers: List[str] = Form(...), swly_bins: List[str] = Form(...), swly_labels: List[str] = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    user = "JQIU"
    
    print("pass")
    # form_data = await request.form()
    # print(form_data)  # Log to see what is received
    # Create a new SWLY_LABEL_DATA record
    new_record = SWLY_LABEL_DATA(
        wafer_id=",".join(wafers),  # Assuming wafer_ids is a list of IDs
        swly_bins=",".join(swly_bins),
        swly_labels=",".join(swly_labels),
        user=user,
        description=description
    )
    
    # # Add the new record to the session and commit it
    db.add(new_record)
    db.commit()
    db.refresh(new_record)  # Refresh to get the ID of the new record
    
    # Return a response 
    
    
    
    
    # # Return a success message along with the ID of the new record
    # return {
    #     "message": "SWLY label data submitted successfully",
    #     "id": new_record.id
    # }
    return JSONResponse(content={"message": "SWLY label data submitted successfully"})