from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Tuple, List, Optional
from app.library.database import get_db
from app.library.models import ACCOUNT_DATA
from typing import Tuple, List, Dict, Annotated, Union
from pydantic import BaseModel
from app.library.helper import CustomJinja2Templates
import jwt
import os 

