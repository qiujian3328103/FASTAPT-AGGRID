
# app/library/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone 
Base = declarative_base()

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
    
