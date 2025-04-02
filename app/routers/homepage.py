from fastapi import FastAPI, Request, Form, APIRouter, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import json 
import pandas as pd 
from typing import Optional
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates
from sqlalchemy.orm import Session 
from app.library.database import get_db
from app.library.models import SWLY_LABEL_LIST, SWLYLabelListUpdate
from datetime import datetime 
from fastapi import HTTPException
from app.routers.auth import User
from app.routers.auth import get_current_username
import csv
from fastapi.responses import StreamingResponse
import io 
from config import TEST_IMAGE_URL
from app.library.models import SWLY_LOW_YIELD_TABLE


router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/homepage", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user = os.getlogin()
    query_result = db.query(SWLY_LOW_YIELD_TABLE).all()
    data = [item.to_dict() for item in query_result]
    df = pd.DataFrame(data)

    # Read CSV data
    # df = pd.read_csv(TEST_DATA_SET_URL)  # Change the path to your CSV file
    
    # Provide initial data for dropdowns
    process_ids = df['lot_id'].unique().tolist()
    step_ids = ["U_SYSREAL_F", "EDS", "FT"]
    sigmas = ["3Sigma", "4Sigma"]
    
    # Convert DataFrame to JSON for ag-Grid
    # column_defs = [{"headerName": col, "field": col} for col in df.columns]
    # Convert DataFrame to JSON for ag-Grid
    column_defs = [
        {"headerName": "Lot ID", "field": "lot_id", "filter": "agSetColumnFilter", "pinned": "left"},
        {"headerName": "Wafer ID", "field": "wafer_id", "filter": "agSetColumnFilter", "pinned": "left"},
        {"headerName": "Yield", "field": "yld", "filter": "agNumberColumnFilter", "filterParams": {"applyButton": True}, "pinned": "left"},
        {"headerName": "Fail Bins", "field": "fail_bin", "filter": "agNumberColumnFilter", "filterParams": {"applyButton": True}, "pinned": "left"},
        {"headerName": "SWLY Marker", "field": "swly_mark", "filter": "agSetColumnFilter", "pinned": "left"},
        {"headerName": "SWLY Label", "field": "swly_label", "filter": "agSetColumnFilter", "pinned": "left"}
    ]
    
    
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # Format the column name (e.g., "W01", "W02", ..., "W25")
        df[col_name] = TEST_IMAGE_URL

    row_data = df.to_dict(orient="records")
    
    # Add a custom cell renderer for each of the new columns
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # Format the column name (e.g., "W01", "W02", ..., "W25")
        column_defs.append({
            "headerName": f"W{i:02d}",
            "field": col_name,
            "cellRenderer": "render_image"
        })
    
        # Provide initial data for dropdowns
    initial_data = {
        "process_ids": df['lot_id'].unique().tolist(),
        "step_ids": ["U_SYSREAL_F", "EDS", "FT"],
        "sigmas": ["3Sigma", "4Sigma"],
        "selected_process_ids": [process_ids[0]],
        "selected_step_id": step_ids[0],
        "selected_sigma": sigmas[0]
    }
    print(initial_data)
    return templates.TemplateResponse("homepage.html", 
                                      {"request": request,
                                       "initial_data": initial_data,
                                       "columnDefs": json.dumps(column_defs), 
                                       "rowData": json.dumps(row_data),
                                       "user": user
                                        })
