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
        {"headerName": "SWLY Label", "field": "swly_label"},
    ]
    row_data = df.to_dict(orient="records")
    return templates.TemplateResponse("createlabel.html", {"request": request, 
                                                           "columnDefs": json.dumps(column_defs), 
                                                           "rowData":json.dumps(row_data)})
    
@router.post("/from_submit_swly_lable", response_class=HTMLResponse)
async def add_or_update_label_data(request: Request, processid_label: str=Form(...), 
                                   swly_label: str=Form(...), user_label: str=Form(...), 
                                   tool_label: Optional[str] = Form(None),
                                   layer_label:Optional[str] = Form(None), 
                                   bin_label:Optional[str] = Form(None), 
                                   signature_label:Optional[str] = Form(None),
                                   type_label:Optional[str] = Form(None),
                                   description: Optional[str] = Form(None),
                                   db: Session=Depends(get_db)
                                   ):
    
    existing_record = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id==processid_label, 
                                                       SWLY_LABEL_LIST.name == swly_label).all()
    
    if existing_record:
        existing_record.process_id = processid_label
        existing_record.layer = layer_label
        existing_record.tool = tool_label
        existing_record.bin_lst = bin_label
        existing_record.signature = signature_label
        existing_record.type = type_label 
        existing_record.desc =  description 
        existing_record.user = user_label
        existing_record.last_update = datetime.now()
    else:
        new_record = SWLY_LABEL_LIST(
                process_id = processid_label,
                layer = layer_label,
                tool = tool_label,
                bin_lst = bin_label,
                signature = signature_label,
                type = type_label,
                desc =  description,
                name = swly_label,
                user = user_label,
                last_update = datetime.now()
        )
        
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
    query_result = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id == processid_label).all()
    row_data = []
    for index, record in enumerate(query_result):
        if record is not None:
            row_data.append({
                "process_id": record.process_id
            })
            
    return JSONResponse(content={"rowData": row_data})