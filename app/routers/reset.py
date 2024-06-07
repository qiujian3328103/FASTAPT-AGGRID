from fastapi import FastAPI, Request, Form, APIRouter, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.library.helper import CustomJinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED
from app.library.database import get_db
from sqlalchemy.orm import Session
from app.library.models import ACCOUNT_DATA
from starlette.authentication import requires
import hashlib

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


@router.get("/reset", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("reset.html", {"request": request})


@router.post("/reset", response_class=HTMLResponse)
async def reset_password(request: Request, email: str = Form(...), current_password: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...), db: Session = Depends(get_db)):
    print(current_password, new_password, confirm_password)
    
    # # Check if the current password matches the stored password for the email
    # user = db.query(ACCOUNT_DATA).filter(ACCOUNT_DATA.email == email).first()
    # if not user or user.password != hash_password(current_password):
    #     raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    # # Check if the new password and confirm password match
    # if new_password != confirm_password:
    #     raise HTTPException(status_code=400, detail="New password and confirm password do not match")

    # # Hash the new password
    # hashed_password = hash_password(new_password)

    # # Update the password in the database
    # user.password = hashed_password
    # db.commit()

    # Redirect to a success page
    return RedirectResponse(url="/reset/success")