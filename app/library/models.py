
# app/library/models.py

from sqlalchemy import Column, Integer, String, DateTime
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
