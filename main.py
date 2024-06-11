from fastapi import FastAPI, Request, Query, Form, Depends, WebSocket

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.library import openfile
from app.library.helper import CustomJinja2Templates
from app.routers import info, twoforms, unsplash, accordion, swly_recorder, lot_review, swly_naming, swly_analysis,swly_listing, login, auth, view_wafermap, reset, page_setting
from app.library.models import SWLY_LOW_YIELD_TABLE
from sqlalchemy.orm import Session 
from app.library.database import get_db
from app.library.websocket_manager import websocket_endpoint, notify_clients

# from starlette.middleware.sessions import SessionMiddleware
# from fastapi_auth_middleware import AuthMiddleware
import pandas as pd 
import json 
import os 
from config import TEST_DATA_SET_URL, TEST_IMAGE_URL
app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

templates = CustomJinja2Templates(directory="templates")
# Adding middleware for session management
# app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY")
# app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)
app.include_router(swly_recorder.router)
app.include_router(lot_review.router)
app.include_router(swly_naming.router)
app.include_router(swly_analysis.router)
app.include_router(swly_listing.router)
app.include_router(info.router)
app.include_router(login.router)
app.include_router(auth.admin_router)
app.include_router(view_wafermap.router)
app.include_router(reset.router)
app.include_router(page_setting.router)
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     data = openfile("home.md")
#     return templates.TemplateResponse("page.html", {"request": request, "data": data})
app.websocket("/ws")(websocket_endpoint)


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user = os.getlogin()
    query_result = db.query(SWLY_LOW_YIELD_TABLE).all()
    data = [item.to_dict() for item in query_result]
    df = pd.DataFrame(data)

    # Read CSV data
    # df = pd.read_csv(TEST_DATA_SET_URL)  # Change the path to your CSV file
    
    # Provide initial data for dropdowns
    process_ids = df['lot_id'].unique().tolist()
    step_ids = ["U_SYSREAL_F", "EDS", "FT"]
    sigmas = ["3Sigma", "4Sigma"]
    
    # Convert DataFrame to JSON for ag-Grid
    # column_defs = [{"headerName": col, "field": col} for col in df.columns]
    # Convert DataFrame to JSON for ag-Grid
    column_defs = [
        {"headerName": "Lot ID", "field": "lot_id", "filter": "agSetColumnFilter", "pinned": "left"},
        {"headerName": "Wafer ID", "field": "wafer_id", "filter": "agSetColumnFilter", "pinned": "left"},
        {"headerName": "Yield", "field": "yld", "filter": "agNumberColumnFilter", "filterParams": {"applyButton": True}, "pinned": "left"},
        {"headerName": "Fail Bins", "field": "fail_bin", "filter": "agNumberColumnFilter", "filterParams": {"applyButton": True}, "pinned": "left"},
        {"headerName": "SWLY Marker", "field": "swly_mark", "filter": "agSetColumnFilter", "pinned": "left"},
        {"headerName": "SWLY Label", "field": "swly_label", "filter": "agSetColumnFilter", "pinned": "left"}
    ]
    
    # Add image URL to the last column ("wafer map")
    # df["wafer map"] = df.apply(lambda row: ["<img src='https://www.kasandbox.org/programming-images/avatars/leaf-blue.png' width='20' height='20'>" for _ in range(5)], axis=1)
    # df["wafer map"] ='https://www.kasandbox.org/programming-images/avatars/leaf-blue.png'
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # Format the column name (e.g., "W01", "W02", ..., "W25")
        # df[col_name] = 'https://www.kasandbox.org/programming-images/avatars/leaf-blue.png'
        df[col_name] = TEST_IMAGE_URL

    row_data = df.to_dict(orient="records")
    
    # Add a custom cell renderer for each of the new columns
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # Format the column name (e.g., "W01", "W02", ..., "W25")
        column_defs.append({
            "headerName": f"W{i:02d}",
            "field": col_name,
            "cellRenderer": "render_image"
        })
    
        # Provide initial data for dropdowns
    initial_data = {
        "process_ids": df['lot_id'].unique().tolist(),
        "step_ids": ["U_SYSREAL_F", "EDS", "FT"],
        "sigmas": ["3Sigma", "4Sigma"],
        "selected_process_ids": [process_ids[0]],
        "selected_step_id": step_ids[0],
        "selected_sigma": sigmas[0]
    }
    
    return templates.TemplateResponse("page.html", 
                                      {"request": request,
                                       "initial_data": initial_data,
                                       "columnDefs": json.dumps(column_defs), 
                                       "rowData": json.dumps(row_data),
                                       "user": user
                                        })



@app.post("/form_submit", response_class=HTMLResponse)
async def update_data(request: Request, processIds: list = Form(...), stepId: str = Form(None), sigma: str = Form(None), 
                      startDate: str = Form(None), endDate: str = Form(None), db: Session = Depends(get_db)):
    print(processIds, stepId, sigma)
    # Read CSV data
    # df = pd.read_csv(TEST_DATA_SET_URL)  # Change the path to your CSV file
    query_result = db.query(SWLY_LOW_YIELD_TABLE).all()
    data = [item.to_dict() for item in query_result]
    df = pd.DataFrame(data)
    
    # Filter DataFrame based on selected process IDs
    filtered_df = df[df['lot_id'].isin(processIds)]
    
    # Convert DataFrame to JSON for ag-Grid
    # column_defs = [{"headerName": col, "field": col} for col in filtered_df.columns]
    
    column_defs = [
        {"headerName": "Lot ID", "field": "lot_id", "filter": "agSetColumnFilter", "pinned": "left","width": 60},
        {"headerName": "Wafer ID", "field": "wafer_id", "filter": "agSetColumnFilter", "pinned": "left","width": 60},
        {"headerName": "Yield", "field": "yld", "filter": "agNumberColumnFilter", "filterParams": {"applyButton": True}, "pinned": "left","width": 60},
        {"headerName": "Fail Bins", "field": "fail_bin", "filter": "agNumberColumnFilter", "filterParams": {"applyButton": True}, "pinned": "left","width": 60},
        {"headerName": "SWLY Marker", "field": "swly_mark", "filter": "agSetColumnFilter", "pinned": "left"},
        {"headerName": "SWLY Label", "field": "swly_label", "filter": "agSetColumnFilter", "pinned": "left","width": 60}
    ]
    
    
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # Format the column name (e.g., "W01", "W02", ..., "W25")
        filtered_df[col_name] = TEST_IMAGE_URL
    
    row_data = filtered_df.to_dict(orient="records")
    
    # Add a custom cell renderer for each of the new columns
    for i in range(1, 26):
        col_name = f"W{i:02d}"  # Format the column name (e.g., "W01", "W02", ..., "W25")
        column_defs.append({
            "headerName": f"W{i:02d}",
            "field": col_name,
            "cellRenderer": "render_image"
        })
    
    # await notify_clients("update")
    # Convert filtered data into JSON structure expected by ag-grid on the frontend
    return JSONResponse(content={"rowData": row_data})


@app.post("/notify_update")
async def notify_update():
    await notify_clients("update")
    return {"message": "Clients notified"}