from fastapi import FastAPI, Request, Form, APIRouter, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import json 
import pandas as pd 
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/label_review", response_class=HTMLResponse)
async def lot_review(request: Request):
    
    df = pd.read_csv("app/Book1.csv")  # Change the path to your CSV file
    
    # Convert DataFrame to JSON for ag-Grid
    # column_defs = [{"headerName": col, "field": col} for col in df.columns]
    # Convert DataFrame to JSON for ag-Grid
    column_defs = [
        {"headerName": "Lot ID", "field": "lot_id"},
        {"headerName": "Wafer ID", "field": "wafer_id"},
        {"headerName": "Yield", "field": "yield"},
        {"headerName": "Fail Bins", "field": "fail_bin"},
        {"headerName": "SWLY Label", "field": "swly_label"}
    ]
    row_data = df.to_dict(orient="records")
    return templates.TemplateResponse("createlabel.html", {"request": request, 
                                                           "columnDefs": json.dumps(column_defs), 
                                                           "rowData":json.dumps(row_data)})
    