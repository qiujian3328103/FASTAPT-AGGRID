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

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/label_review", response_class=HTMLResponse)
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
                })
    
    # column_defs = [
    #     {"headerName": "process_id", "field": "process_id"},
    #     {"headerName": "layer", "field": "layer"},
    #     {"headerName": "EQP", "field": "tool"},
    #     {"headerName": "Bins", "field": "bin_lst"},
    #     {"headerName": "Signature", "field": "signature"},
    #     {"headerName": "Type", "field": "type"},
    #     {"headerName": "SWLY_Name", "field": "name"},
    #     {"headerName": "Desc", "field": "desc"},
    #     {"headerName": "User", "field": "user"},
    #     {"headerName": "Last Update", "field": "last_update"},
    # ]
    return templates.TemplateResponse("createlabel.html", {"request": request, 
                                                           "rowData":json.dumps(row_data)})


from fastapi import HTTPException, status

@router.post("/submit_swly_list_data", response_model=List[SWLYLabelListUpdate])
async def add_or_update_label_data(
    request: Request,
    processid_label: str = Form(...),
    swly_label: str = Form(...),
    user_label: str = Form(...),
    tool_label: Optional[str] = Form(None),
    layer_label: Optional[str] = Form(None),
    bin_label: Optional[str] = Form(None),
    signature_label: Optional[str] = Form(None),
    type_label: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_username)
):
    # Check user authorization first
    if current_user.auth == "Reader":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to edit")

    # Retrieve the existing record or None
    existing_record = db.query(SWLY_LABEL_LIST).filter(
        SWLY_LABEL_LIST.process_id == processid_label,
        SWLY_LABEL_LIST.name == swly_label
    ).first()

    # Update or create new record
    if existing_record:
        existing_record.layer = layer_label or existing_record.layer
        existing_record.tool = tool_label or existing_record.tool
        existing_record.bin_lst = bin_label or existing_record.bin_lst
        existing_record.signature = signature_label or existing_record.signature
        existing_record.type = type_label or existing_record.type
        existing_record.desc = description or existing_record.desc
        existing_record.user = user_label or existing_record.user
        existing_record.last_update = datetime.now()
    else:
        new_record = SWLY_LABEL_LIST(
            process_id=processid_label,
            layer=layer_label,
            tool=tool_label,
            bin_lst=bin_label,
            signature=signature_label,
            type=type_label,
            name=swly_label,
            user=user_label,
            desc=description,
            last_update=datetime.now()
        )
        db.add(new_record)

    db.commit()

    # Re-fetch the data to ensure consistency and send it back to the client
    updated_records = db.query(SWLY_LABEL_LIST).filter(
        SWLY_LABEL_LIST.process_id == processid_label
    ).order_by(SWLY_LABEL_LIST.last_update.desc()).all()

    return [record.to_dict() for record in updated_records]



# @router.post("/submit_swly_list_data", response_class=HTMLResponse)
# async def add_or_update_label_data(request: Request, 
    #                                processid_label: str = Form(...), 
    #                                swly_label: str = Form(...),
    #                                user_label: str = Form(...), 
    #                                tool_label: Optional[str] = Form(None),
    #                                layer_label: Optional[str] = Form(None), 
    #                                bin_label: Optional[str] = Form(None), 
    #                                signature_label: Optional[str] = Form(None),
    #                                type_label:Optional[str] = Form(None),
    #                                description: Optional[str] = Form(None),
    #                                db: Session=Depends(get_db),
    #                                current_user: User = Depends(get_current_username)
    #                                ):
    # if current_user.auth not in ["Reader", "Admin", "Editor"]:
    #     raise HTTPException(status_code=403, detail="User not authorized to edit")
    # try:
    #     existing_record = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id==processid_label, 
    #                                                     SWLY_LABEL_LIST.name == swly_label).first()  
    #     if existing_record:
    #         existing_record.process_id = processid_label
    #         existing_record.layer = layer_label
    #         existing_record.tool = tool_label
    #         existing_record.bin_lst = bin_label
    #         existing_record.signature = signature_label
    #         existing_record.type = type_label 
    #         existing_record.desc =  description 
    #         existing_record.user = user_label
    #         existing_record.last_update = datetime.now()
    #         db.commit()
    #     else:
    #         new_record = SWLY_LABEL_LIST(
                
    #                 process_id = processid_label,
    #                 layer = layer_label,
    #                 tool = tool_label,
    #                 bin_lst = bin_label,
    #                 signature = signature_label,
    #                 type = type_label,
    #                 desc =  description,
    #                 name = swly_label,
    #                 user = user_label,
    #                 last_update = datetime.now()
    #         )
            
    #         db.add(new_record)
    #         db.commit()
    #         print("New record added with ID:", new_record.id)
    #         # db.refresh(new_record)
            
    #     query_result = db.query(SWLY_LABEL_LIST).filter(SWLY_LABEL_LIST.process_id == processid_label).all()
    #     row_data = []
    #     for index, record in enumerate(query_result):
    #         if record is not None:
    #             row_data.append({
    #                 "process_id": record.process_id,
    #                 "layer": record.layer,
    #                 "tool": record.tool,
    #                 "bin_lst": record.bin_lst,
    #                 "signature": record.signature,
    #                 "type": record.type,
    #                 "name": record.name,
    #                 "desc": record.desc,
    #                 "user": record.user, 
    #                 "last_update": record.last_update.strftime("%Y-%m-%d"),
    #             })
                
    #     return JSONResponse(content={"rowData": row_data})
    # except Exception as e:
    #     return JSONResponse(status_code=400, content={"message": str(e)})