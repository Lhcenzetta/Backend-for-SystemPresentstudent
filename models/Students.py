from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Student(Base):
    __tablename__ = "students"

    first_name     = Column(String(100), nullable=False)
    last_name      = Column(String(100), nullable=False)
    apogee_code    = Column(String(20), primary_key=True)
    cin_passport   = Column(String(20), unique=True, nullable=False)
    field_of_study = Column(String(100), nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    apogee_code    = Column(String(20), ForeignKey("students.apogee_code"), nullable=False)
    full_name      = Column(String(200), nullable=False)
    date_pointage  = Column(Date, default=func.current_date())
    heure_pointage = Column(Time, default=func.current_time())
    logs_today     = Column(Integer, default=1)

    student        = relationship("Student", backref="attendances")