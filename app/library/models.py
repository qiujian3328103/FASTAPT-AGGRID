
# app/library/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone 
from typing import Optional, List
from pydantic import BaseModel 
from starlette.authentication import BaseUser

Base = declarative_base()

class FastAPIUser(BaseUser):
    def __init__(self, email: str, scopes: List[str]):
        self.email = email
        self.scopes = scopes

    @property
    def identity(self):
        return self.email

    def __str__(self):
        return self.email


class SWLYLabelListUpdate(BaseModel):
    process_id: Optional[str]
    layer: Optional[str]
    tool: Optional[str]
    bin_lst: Optional[str]
    signature: Optional[str]
    type: Optional[str]
    name: Optional[str]
    desc: Optional[str]
    user: Optional[str]
    last_update: Optional[datetime]

class ACCOUNT_DATA(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    auth = Column(String)
    last_update = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name, 
            "last_name": self.last_name, 
            "email": self.email,
            "auth": self.auth,
            "last_update": self.last_update.isoformat() if self.last_update else None
        }
    

class SWLY_LABEL_DATA(Base):
    __tablename__ = "swly_label_data"

    id = Column(Integer, primary_key=True, index=True)
    wafer_id = Column(String, index=True)
    swly_bins = Column(String)
    swly_labels = Column(String)
    description = Column(String)
    user = Column(String)
    edit_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Use timezone-aware datetime
    
    
class SWLY_LABEL_LIST(Base):
    __tablename__ = "swly_name_table"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    process_id = Column(String)
    layer = Column(String)
    tool = Column(String)
    bin_lst = Column(String)
    signature = Column(Text)
    type = Column(String)
    name = Column(String)
    user = Column(String)
    desc = Column(String)
    last_update = Column(DateTime, default=lambda: datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "process_id": self.process_id,
            "layer": self.layer,
            "tool": self.tool,
            "bin_lst": self.bin_lst,
            "signature": self.signature,
            "type": self.type,
            "name": self.name,
            "desc": self.desc,
            "user": self.user,
            "last_update": self.last_update.strftime("%Y-%m-%d %H:%M:%S") if self.last_update else None
        }
    
class SWLY_COLOR_LIST(Base):
    __tablename__ = "BIN_COLOR_TABLE"
    id = Column(Integer, primary_key=True, autoincrement=True)
    process_id = Column(String)
    bin = Column(String)
    bin_group = Column(String)
    color = Column(String)
    
    def to_dict(self):
        return {
            "id": self.id,
            "process_id": self.process_id,
            "bin": self.bin,
            "bin_group": self.bin_group,
            "color": self.color,
        }
    
class SWLY_LOW_YIELD_TABLE(Base):
    __tablename__ = "low_yield_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id = Column(String)
    wafer_id = Column(String)
    yld = Column(String)
    fail_bin = Column(String)
    swly_mark = Column(String)
    swly_label = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "lot_id": self.lot_id,
            "wafer_id": self.wafer_id,
            "yld": self.yld,
            "fail_bin": self.fail_bin,
            "swly_mark": self.swly_mark,
            "swly_label": self.fail_bin,
        }
    
    
class ProductInfo(Base):
    __tablename__ = "product_info"
    
    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(String, index=True)
    step_seq = Column(Integer)
    pgm_id = Column(String)
