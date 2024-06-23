from fastapi import FastAPI, Request, APIRouter, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel
import pandas as pd 
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")

class LotIdQueryParams(BaseModel):
    process_ids: List[str]
    labels: List[str]

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
async def get_lot_ids(params: LotIdQueryParams = Depends()):
    df = pd.DataFrame(
        {'process_id': ["process_1", "process_1", "process_1", "process_2", "process_2", "process_2", "process_3"], 
         'label': ["label1", "label2", "label3", "label4", "label1", "label2", "label3"], 
         'lot_id': ["lot1", "lot1", "lot2", "lot3", "lot4", "lot5", "lot6"]
        }
    )

    filtered_df = df[df['process_id'].isin(params.process_ids) & df['label'].isin(params.labels)]
    lot_ids = filtered_df['lot_id'].unique().tolist()

    return {"lot_ids": lot_ids}
