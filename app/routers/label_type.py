from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List

from database import SessionLocal, init_db
from models import Signature, Label

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_signatures(request: Request, db: Session = Depends(get_db)):
    signatures = db.query(Signature).all()
    return templates.TemplateResponse("index.html", {"request": request, "signatures": signatures})

@app.post("/signatures/", response_class=JSONResponse)
async def create_signature(signature_type: str = Form(...), db: Session = Depends(get_db)):
    db_signature = Signature(signature_type=signature_type)
    db.add(db_signature)
    db.commit()
    db.refresh(db_signature)
    return {"id": db_signature.id, "signature_type": db_signature.signature_type}

@app.put("/signatures/{signature_id}", response_class=JSONResponse)
async def update_signature(signature_id: int, signature_type: str = Form(...), db: Session = Depends(get_db)):
    db_signature = db.query(Signature).filter(Signature.id == signature_id).first()
    if not db_signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    db_signature.signature_type = signature_type
    db.commit()
    db.refresh(db_signature)
    return {"id": db_signature.id, "signature_type": db_signature.signature_type}

@app.delete("/signatures/{signature_id}", response_class=JSONResponse)
async def delete_signature(signature_id: int, db: Session = Depends(get_db)):
    db_signature = db.query(Signature).filter(Signature.id == signature_id).first()
    if not db_signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    db.delete(db_signature)
    db.commit()
    return {"detail": "Signature deleted"}

# New CRUD operations for label_type
@app.get("/labels", response_class=HTMLResponse)
async def read_labels(request: Request, db: Session = Depends(get_db)):
    labels = db.query(Label).all()
    return templates.TemplateResponse("labels.html", {"request": request, "labels": labels})

@app.post("/labels/", response_class=JSONResponse)
async def create_label(label_type: str = Form(...), db: Session = Depends(get_db)):
    db_label = Label(label_type=label_type)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return {"id": db_label.id, "label_type": db_label.label_type}

@app.put("/labels/{label_id}", response_class=JSONResponse)
async def update_label(label_id: int, label_type: str = Form(...), db: Session = Depends(get_db)):
    db_label = db.query(Label).filter(Label.id == label_id).first()
    if not db_label:
        raise HTTPException(status_code=404, detail="Label not found")
    db_label.label_type = label_type
    db.commit()
    db.refresh(db_label)
    return {"id": db_label.id, "label_type": db_label.label_type}

@app.delete("/labels/{label_id}", response_class=JSONResponse)
async def delete_label(label_id: int, db: Session = Depends(get_db)):
    db_label = db.query(Label).filter(Label.id == label_id).first()
    if not db_label:
        raise HTTPException(status_code=404, detail="Label not found")
    db.delete(db_label)
    db.commit()
    return {"detail": "Label deleted"}
