from fastapi import FastAPI, Request, Form, APIRouter, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import json 
import pandas as pd 
from typing import Optional
from io import StringIO
import csv
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates
from sqlalchemy.orm import Session 
from app.library.database import get_db, SessionLocal
from app.library.models import SWLY_LABEL_LIST, ProductInfo
from datetime import datetime 
from config import TEST_LABEL_DATA


router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


# 上传页面路由
@router.get("/upload")
def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# 处理上传数据
@router.post("/upload")
async def upload_csv_data(request: Request, csvData: str = Form(...)):
    if not csvData.strip():
        return templates.TemplateResponse("upload.html", {
            "request": request, 
            "message": "No data provided"
        })
    
    # 解析CSV数据
    csv_file = StringIO(csvData)
    csv_reader = csv.reader(csv_file)
    
    # 创建数据库会话
    db = SessionLocal()
    try:
        count = 0
        for row in csv_reader:
            if len(row) >= 3:
                try:
                    product_info = ProductInfo(
                        process_id=row[0],
                        step_seq=int(row[1]),
                        pgm_id=row[2]
                    )
                    db.add(product_info)
                    count += 1
                except ValueError:
                    # 跳过无效行
                    continue
        
        db.commit()
        return templates.TemplateResponse("upload.html", {
            "request": request, 
            "message": f"Successfully uploaded {count} rows of data"
        })
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("upload.html", {
            "request": request, 
            "message": f"Upload failed: {str(e)}"
        })
    finally:
        db.close()