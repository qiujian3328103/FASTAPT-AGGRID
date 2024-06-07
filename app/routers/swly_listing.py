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

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/swly_list", response_class=HTMLResponse)
async def lot_review(request: Request, db:Session=Depends(get_db)):

    process = db.query(SWLY_LABEL_LIST.process_id).distinct().all()
    process_ids = [row.process_id for row in process]
    query_result = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id==process_ids[0]).order_by(SWLY_LABEL_LIST.last_update.desc()).all()
    
    row_data = []
    
    if not query_result:
        print("No records found for root_lot_id}")
    else:
        for index, record in enumerate(query_result):
            if record is not None:
                # Parse the bin_lst and generate image paths
                bin_numbers = record.layer.split(',')
                image_paths = ','.join([f"static/images/map.jpg" for bin in bin_numbers])
                
                row_data.append({
                    "process_id": record.process_id,
                    "layer": record.layer,
                    "tool": record.tool,
                    "bin_lst": record.bin_lst,
                    "signature": record.signature,
                    "type": record.type,
                    "name": record.name,
                    "desc": record.desc,
                    "user": record.user, 
                    "last_update": record.last_update.strftime("%Y-%m-%d"),
                    "image":image_paths
                })
                
    return templates.TemplateResponse("listview.html", {"request": request, 
                                                           "rowData":json.dumps(row_data)})
    
@router.put("/edit_row/{process_id}/{name}")
async def edit_row(process_id: str, name: str, item: SWLYLabelListUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_username)):
    print(current_user)
    if current_user.auth in ["Admin"]:
        raise HTTPException(status_code=403, detail="User not authorized to edit")
    else:
        db_item = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id == process_id, SWLY_LABEL_LIST.name == name).first()        
        if db_item:
            # Here, update fields if they are provided in the request
            db_item.name = item.name if item.name else db_item.name
            db_item.desc = item.desc if item.desc else db_item.desc
            db_item.user = item.user if item.user else db_item.user
            # Repeat for other fields...
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/delete_row/{process_id}/{name}")
async def delete_row(process_id: str, name: str, db: Session = Depends(get_db)):
    # your deletion logic here
    db_item = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id == process_id, SWLY_LABEL_LIST.name == name).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.get("/swly_list_reload", response_class=JSONResponse)
async def lot_review(request: Request, db: Session = Depends(get_db)):
    process = db.query(SWLY_LABEL_LIST.process_id).distinct().all()
    process_ids = [row.process_id for row in process]
    query_result = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id == process_ids[0]).order_by(SWLY_LABEL_LIST.last_update.desc()).all()

    row_data = [record.to_dict() for record in query_result]  # Convert SQLAlchemy models to dictionaries

    return row_data  # Ensure this returns a list of dicts directly


@router.get("/download_csv")
async def download_csv(db: Session = Depends(get_db)):
    query_result = db.query(SWLY_LABEL_LIST).all()

    def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        # Write header
        writer.writerow(['process_id', 'layer', 'tool', 'bin_lst', 'signature', 'type', 'name', 'desc', 'user', 'last_update'])
        # Write data
        for record in query_result:
            writer.writerow([
                record.process_id,
                record.layer,
                record.tool,
                record.bin_lst,
                record.signature,
                record.type,
                record.name,
                record.desc,
                record.user,
                record.last_update.strftime("%Y-%m-%d")
            ])
        output.seek(0)
        yield output.read()

    return StreamingResponse(generate_csv(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=swly_label_list.csv"})