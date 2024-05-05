from fastapi import FastAPI, Request, Form, APIRouter, Query, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import json 
import pandas as pd 
from typing import Optional, List
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates
from sqlalchemy.orm import Session 
from app.library.database import get_db
from app.library.models import SWLY_LABEL_LIST, SWLYLabelListUpdate
from app.routers.auth import get_current_username, User
from datetime import datetime 
from pydantic import BaseModel
from app.library.utilies import create_wafer_data

class SubmitWaferMapRequest(BaseModel):
    root_lot_id: str 
    step_id: str 
    startDate: Optional[str] 
    endDate: Optional[str]

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/wafermap", response_class=HTMLResponse)
async def wafer_review(request: Request):
    step_id = ["Step1", "Stpe2", "Step3"]
    root_lot_id = "AAAAA"
    return templates.TemplateResponse("wafermap.html", {"request": request,
                                                        "step_ids": step_id,
                                                        "root_lot_id":root_lot_id,
                                                        "wafer_range": 25})
    

@router.post("/UpdateWaferMap", response_class=JSONResponse)
async def update_wafermap(request: Request,item: SubmitWaferMapRequest):
    print(item)
    root_lot_id = item.root_lot_id
    step_id = item.step_id
    start_date = item.startDate
    end_date = item.endDate

    # Assuming create_wafer_data function is implemented correctly and can handle the inputs
    wafer_data, shot_data, width, height = create_wafer_data(root_lot_id)

    return {"waferData": wafer_data, "shotData": shot_data, "width": width, "height": height}