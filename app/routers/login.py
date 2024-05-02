from fastapi import FastAPI, Request, Form, APIRouter, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.library.helper import CustomJinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED
from app.library.database import get_db
from sqlalchemy.orm import Session
from app.library.models import ACCOUNT_DATA
from starlette.authentication import requires

router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


def authenticate_user(username: str, password: str):
    # This should be replaced with a proper authentication mechanism
    if username == "jian.qiu@gmail.com" and password == "admin":
        return True
    return False


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    print(email, password)
    user_authenticated = authenticate_user(email, password)
    if not user_authenticated:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        # If authentication is successful, set the user session
        return RedirectResponse(url="/admin", status_code=302)
    

    # if request.session.get("is_authenticated"):
    #     # Fetch all accounts from the database
    #     accounts = db.query(ACCOUNT_DATA).all()
    #     account_data = [account.to_dict() for account in accounts]
    #     # Pass the accounts data to the template
    #     return templates.TemplateResponse("admin.html", {
    #         "request": request,
    #         "accounts": account_data  # Adding accounts data to the context
    #     })
    # else:
    #     return RedirectResponse(url="/login", status_code=302)
