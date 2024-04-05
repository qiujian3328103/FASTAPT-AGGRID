from fastapi import FastAPI, Request, Form, APIRouter, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import pandas as pd 
from app.library.helper import openfile

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/lot_review", response_class=HTMLResponse)
async def lot_review(request: Request, lot_id: str = Query(...), wafer_id: str = Query(...)):
    print(lot_id, wafer_id)
    df = pd.read_csv("app/Book1.csv")  # Change the path to your CSV file
    
    filtered_df = df[df["lot_id"]==lot_id]
    
    lot_wafer_urls = []
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # This variable isn't used in your snippet but might be intended for something else?
        lot_wafer_urls.append({"lot_wafer": f"{lot_id}_{wafer_id}",
                            "image": 'static/images/map.jpg'})
    
    print(lot_wafer_urls)
    
    return templates.TemplateResponse("lotreview.html", {"request": request, 
                                                          "lot_wafer_urls":lot_wafer_urls})

    
    
    