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
    df['month'] = df['edit_date'].dt.to_period('M')
    grouped = df.groupby(['swly_label', 'month'])['wafer_counts'].sum().unstack(fill_value=0)
    data = grouped.transpose().to_json()
    return templates.TemplateResponse("analysispage.html", {"request": request,"data":data})