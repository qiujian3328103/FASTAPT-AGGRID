from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.library.database import get_db
from admin.libaray.model import User
from admin.libaray.hashing import Hasher
from sqlalchemy.exc import IntegrityError
from app.library.helper import CustomJinja2Templates
router = APIRouter()
templates = CustomJinja2Templates(directory="templates")


@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse("userregister.html", {"request": request})


@router.post("/register")
async def registration(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not password or len(password) < 6:
        errors.append("Password should be greater than 6 chars")
    if not email:
        errors.append("Email can't be blank")
    user = User(email=email, password=Hasher.get_hash_password(password))
    if len(errors) > 0:
        return templates.TemplateResponse(
            "userregister.html", {"request": request, "errors": errors}
        )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return responses.RedirectResponse(
            "/?msg=successfully registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("Duplicate email")
        return templates.TemplateResponse(
            "userregister.html", {"request": request, "errors": errors}
        )