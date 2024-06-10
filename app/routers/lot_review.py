from fastapi import FastAPI, Request, Form, APIRouter, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import pandas as pd 
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates
from config import TEST_DATA_SET_URL
router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/lot_review", response_class=HTMLResponse)
async def lot_review(request: Request, lot_id: str = Query(...), wafer_id: str = Query(...)):
    print(lot_id, wafer_id)
    df = pd.read_csv(TEST_DATA_SET_URL)  # Change the path to your CSV file
    
    filtered_df = df[df["lot_id"]==lot_id]
    
    lot_wafer_urls = []
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # This variable isn't used in your snippet but might be intended for something else?
        lot_wafer_urls.append({"lot_wafer": f"{lot_id}_{wafer_id}",
                            "image": 'static/images/map.jpg'})
    
    print(lot_wafer_urls)
    
    return templates.TemplateResponse("lotreview.html", {"request": request, 
                                                          "lot_wafer_urls":lot_wafer_urls})
    

@router.get("/form_lotreview_submit", response_class=HTMLResponse)
async def update_lot_review(request: Request, lot_id: str = Query(...)):
    print(lot_id)
    df = pd.read_csv(TEST_DATA_SET_URL)  # Change the path to your CSV file
    
    filtered_df = df[df["lot_id"]==lot_id]
    
    lot_wafer_urls = []
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # This variable isn't used in your snippet but might be intended for something else?
        lot_wafer_urls.append({"lot_wafer": f"{lot_id}_{col_name}",
                            "image": 'static/images/SWLY.jpg'})
    
    print(lot_wafer_urls)
    return JSONResponse(content={"lot_wafer_urls": lot_wafer_urls})
    

    
    
    