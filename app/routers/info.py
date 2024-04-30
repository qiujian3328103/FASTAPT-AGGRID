from fastapi import FastAPI, Request, Form, APIRouter, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import pandas as pd 
from app.library.helper import openfile
from app.library.helper import CustomJinja2Templates

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")

@router.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("markdown.html", {"request": request, "data": data})