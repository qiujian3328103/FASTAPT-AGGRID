from fastapi import FastAPI, Request, APIRouter, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import pandas as pd 
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")

class LotIdQueryParams(BaseModel):
    process_ids: List[str] = Query(...)
    labels: List[str] = Query(...)

@router.get("/alarm_analysis", response_class=HTMLResponse)
async def show_page(request: Request):
    df = pd.DataFrame(
        {'process_id': ["process_1", "process_1", "process_1", "process_2", "process_2", "process_2", "process_3"], 
         'label': ["label1", "label2", "label3", "label4", "label1", "label2", "label3"], 
         'lot_id': ["lot1", "lot1", "lot2", "lot3", "lot4", "lot5", "lot6"]
        }
    )

    initial_data = {
        "process_ids": df["process_id"].unique().tolist(),
        "labels": df["label"].unique().tolist(), 
        "areas": ["CVD", "PVD", "DIFF", "PHOTO", "DEFECT", "METRO", "ETCH"],
        "selected_process_ids": ["process_1", "process_2"]
    }

    return templates.TemplateResponse("alarm.html", {"request": request, "initial_data": initial_data})

@router.get("/get_lot_ids")
async def get_lot_ids(
    process_ids: List[str] = Query(...),
    labels: List[str] = Query(...)
):
    df = pd.DataFrame(
        {'process_id': ["process_1", "process_1", "process_1", "process_2", "process_2", "process_2", "process_3"], 
         'label': ["label1", "label2", "label3", "label4", "label1", "label2", "label3"], 
         'lot_id': ["lot1", "lot1", "lot2", "lot3", "lot4", "lot5", "lot6"]
        }
    )

    filtered_df = df[df['process_id'].isin(process_ids) & df['label'].isin(labels)]
    lot_ids = filtered_df['lot_id'].unique().tolist()

    return {"lot_ids": lot_ids}

@router.get("/get_area_data")
async def get_area_data(area: str):
    # Simulate reading from CSV for the given area
    df = pd.read_csv(f'{area}.csv')  # Assuming each area has its own CSV file
    column_defs = [{"headerName": col, "field": col} for col in df.columns]
    row_data = df.to_dict(orient='records')

    return {"columnDefs": column_defs, "rowData": row_data}
