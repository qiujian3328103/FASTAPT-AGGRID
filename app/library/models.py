
# app/library/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone 
from typing import Optional
from pydantic import BaseModel 
Base = declarative_base()


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
    
