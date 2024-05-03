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

class UpdateUser(BaseModel):
    user_id: str 
    first_name: str 
    last_name: str 
    email: str 
    auth: str 
    password: Optional[str]

# this is the schema 
class User(BaseModel):
    user_id : str 
    email: str 
    auth: str
    password: Optional[str]
    
# Assuming 'get_db' is your dependency that provides a session
def get_current_username(db: Session = Depends(get_db)) -> User:
    # user_id = os.getenv("USER")  # Assuming you get the UNIX username from the environment
    user_id = os.getlogin() 
    account = db.query(ACCOUNT_DATA).filter(ACCOUNT_DATA.user_id == user_id).first()
    if account:
        return User(user_id=account.user_id, email=account.email, auth=account.auth)
    else:
        return User(user_id=account.user_id, email="", auth="Reader")

    
class PermissionCheck:
    def __init__(self) -> None:
        self._allow_users = ["root", "jian.qiu", "JianQiu"]
        
    def __call__(self, current_user: User = Depends(get_current_username)):
        print("-----------------")
        print(current_user)
        permission_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "user doe not have the required permission"
        )
    
        if not current_user.user_id in self._allow_users:
            raise permission_exception
        
has_permission = PermissionCheck()
admin_router = APIRouter(dependencies=[Depends(has_permission)])
templates = CustomJinja2Templates(directory="templates")

@admin_router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, db: Session = Depends(get_db)):
    accounts = db.query(ACCOUNT_DATA).all()
    account_data = [account.to_dict() for account in accounts]
    # Pass the accounts data to the template
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "accounts": account_data  # Adding accounts data to the context
    })

@admin_router.put("/edit_admin/{user_id}", response_class=JSONResponse)
async def edit_row(user_id: str, item: UpdateUser, db: Session = Depends(get_db)):
    db_item = db.query(ACCOUNT_DATA).filter(ACCOUNT_DATA.user_id == user_id).first()
    if db_item:
        db_item.first_name = item.first_name or db_item.first_name
        db_item.last_name = item.last_name or db_item.last_name
        db_item.auth = item.auth or db_item.auth
        db_item.email = item.email or db_item.email
        db.commit()
        return {"status": "success", "message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@admin_router.get("/admin_reload", response_class=JSONResponse)
async def lot_review(request: Request, db: Session = Depends(get_db)):
    query_result = db.query(ACCOUNT_DATA).all()
    row_data = [record.to_dict() for record in query_result]
    return row_data
     
             