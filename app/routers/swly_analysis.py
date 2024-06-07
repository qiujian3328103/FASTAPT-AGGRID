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
from app.library.models import SWLY_LABEL_LIST
from datetime import datetime 

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/swly_analysis", response_class=HTMLResponse)
async def lot_review(request: Request):
    df = pd.read_csv("app/plot_test_data.csv", index_col=False)
    df["edit_date"] = pd.to_datetime(df["edit_date"])
    df['month'] = df['edit_date'].dt.strftime('%Y-%m')  # Use month-year format

    # Data for bar chart
    df_bar = df.copy()
    df_bar['month_period'] = df_bar['edit_date'].dt.to_period('M')
    grouped_bar = df_bar.groupby(['swly_label', 'month_period'])['wafer_counts'].sum().unstack(fill_value=0)
    bar_data = grouped_bar.transpose().to_json()

    # Data for line chart
    df_line = df.groupby(['swly_label', 'month'])['swly_percent'].mean().reset_index()
    line_data = df_line.to_json(orient='records')  # Send data in a simple array of objects

    return templates.TemplateResponse("analysispage.html", {"request": request,"bar_data":bar_data, "line_data": line_data})


@router.post("/filter_data/{label}", response_class=JSONResponse)
async def filter_data(request: Request, label: Optional[str] = None, db: Session = Depends(get_db)):
    print(label)
    df = pd.read_csv("app/plot_test_data.csv", index_col=False)
    df["edit_date"] = pd.to_datetime(df["edit_date"])
    df['month'] = df['edit_date'].dt.strftime('%Y-%m')  # Use month-year format

    # Filter data based on the label
    df_filtered = df[df['swly_label'].str.contains(label, case=False, na=False)]

    # Data for bar chart
    df_bar = df_filtered.copy()
    df_bar['month_period'] = df_bar['edit_date'].dt.to_period('M')
    grouped_bar = df_bar.groupby(['swly_label', 'month_period'])['wafer_counts'].sum().unstack(fill_value=0)
    grouped_bar.columns = grouped_bar.columns.astype(str)  # Convert Period index to string
    bar_data = grouped_bar.transpose().to_dict()

    # Data for line chart
    df_line = df_filtered.groupby(['swly_label', 'month'])['swly_percent'].mean().reset_index()
    line_data = df_line.to_dict(orient='records')  # Send data in a simple array of objects

    return JSONResponse({"bar_data": bar_data, "line_data": line_data})