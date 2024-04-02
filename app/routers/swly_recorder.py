from fastapi import FastAPI, Request, Form, APIRouter, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from bokeh.plotting import figure
from bokeh.embed import components
import pandas as pd 

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


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
    df_raw = pd.read_csv(r"C:\Users\Jian Qiu\Dropbox\pythonprojects\django_web1\sample.csv", index_col=False)
    # Filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001

    df['left'] = df['ucs_die_origin_x']*0.001 
    df['right'] = df['ucs_die_origin_x']*0.001
    df['bottom'] = df['ucs_die_origin_y'] *0.001
    df['top'] = df['ucs_die_origin_y']*0.001
    # Setting the width and height

    # Map the ucs_die_origin_x and ucs_die_origin_y to x and y, and set color
    df["color"] = "green"
    
    # Generate a list of dictionaries to match the format needed for D3.js
    wafer_data = df.apply(lambda row: {
        "x": row["left"],
        "y": row["bottom"],
        "color": row["color"],
        "mouseover": f"Die_x: {int(row['sort_die_x'])}\nDie_y: {int(row['sort_die_y'])}"
    }, axis=1).tolist()
    return templates.TemplateResponse("waferlabel.html", 
                                      {"request": request, 
                                       "lot_id": lot_id, 
                                       "wafer_id": wafer_id,
                                       "waferData": wafer_data,
                                       "rectWidth": width,
                                       "rectHeight": height
                                       })
