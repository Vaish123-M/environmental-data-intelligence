from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

DATABASE_URL = "sqlite:///./environmental_data.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class EnvironmentalData(Base):
    __tablename__ = "environmental_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    region = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    rainfall = Column(Float)
    aqi = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
