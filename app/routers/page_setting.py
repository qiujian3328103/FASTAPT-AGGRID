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
from app.library.models import SWLY_COLOR_LIST
from datetime import datetime 
from config import TEST_LABEL_DATA
from app.library.schema import ColorSearchForm

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")

@router.get("/setting", response_class=HTMLResponse)
async def setting_page(request: Request, db:Session=Depends(get_db)):
    process = db.query(SWLY_COLOR_LIST.process_id).distinct().all()
    process_ids = [row.process_id for row in process]

    initial_data = {
        "process_ids": process_ids,
        "selected_process_ids": process_ids[0]
    }

    row_data = []
    query_result = db.query(SWLY_COLOR_LIST).filter(SWLY_COLOR_LIST.process_id==process_ids[0]).order_by(SWLY_COLOR_LIST.bin).all()
    if not query_result:
        print("No records found for root_lot_id}")
    else:
        for index, record in enumerate(query_result):
            if record is not None:
                row_data.append({
                    "process_id": record.process_id,
                    "bin": record.bin,
                    "bin_group": record.bin_group,
                    "color": record.color
                })

    return templates.TemplateResponse("setting.html", {"request": request,"initial_data": initial_data, "row_data": row_data})


@router.post("/update_color")
async def update_color(data: dict, db: Session = Depends(get_db)):
    process_id = data.get('process_id')
    bin = data.get('bin')
    new_color = data.get('color')

    if not process_id or not bin or not new_color:
        return JSONResponse(content={"success": False, "message": "Invalid data"}, status_code=400)

    color_record = db.query(SWLY_COLOR_LIST).filter_by(process_id=process_id, bin=bin).first()
    if color_record:
        color_record.color = new_color
        db.commit()
        return JSONResponse(content={"success": True, "message": "Color updated successfully"})

    return JSONResponse(content={"success": False, "message": "Record not found"}, status_code=404)

@router.post("/filter_color")
async def filter_data(item: ColorSearchForm, db: Session = Depends(get_db)):
    process_id = item.process_id
    row_data = []
    query_result = db.query(SWLY_COLOR_LIST).filter(SWLY_COLOR_LIST.process_id == process_id).order_by(SWLY_COLOR_LIST.bin).all()
    if not query_result:
        print(f"No records found for process_id {process_id}")
    else:
        for record in query_result:
            row_data.append({
                "process_id": record.process_id,
                "bin": record.bin,
                "bin_group": record.bin_group,
                "color": record.color
            })
    return JSONResponse(content=row_data)