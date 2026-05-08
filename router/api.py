from datetime import datetime, date, timedelta
from fastapi import Depends ,APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.database import engine, get_db
from models.Students import Student
from schema.student_id import StudentID
from models.Students import Attendance
router = APIRouter()



@router.post("/attendance/log")
def log_attendance(data: StudentID, db: Session = Depends(get_db)):
    sid = data.apogee_code

    # 1. Check if student exists
    student = db.query(Student).filter(Student.apogee_code == sid).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 2. Get all logs for today
    today = date.today()
    today_logs = db.query(Attendance).filter(
        Attendance.apogee_code == sid,
        Attendance.date_pointage == today
    ).order_by(Attendance.heure_pointage).all()

    now = datetime.now()
    current_time = now.time().replace(second=0, microsecond=0)

    
    if len(today_logs) >= 4:
        raise HTTPException(
            status_code=409,
            detail={
                "status": "limit_reached",
                "message": f"{student.first_name} {student.last_name} already logged 4 times today",
            }
        )


    if today_logs:
        last_log_time = datetime.combine(today, today_logs[-1].heure_pointage)
        diff = now - last_log_time
        if diff < timedelta(hours=2):
            remaining = timedelta(hours=2) - diff
            minutes_left = int(remaining.total_seconds() / 60)
            raise HTTPException(
                status_code=409,
                detail={
                    "status": "too_soon",
                    "message": f"Must wait at least 2 hours between logs",
                    "minutes_remaining": minutes_left
                }
            )

    new_log = Attendance(
        apogee_code=sid,
        full_name=f"{student.first_name} {student.last_name}",
        date_pointage=today,
        heure_pointage=current_time,
        logs_today=len(today_logs) + 1
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {
        "status": "success",
        "student": f"{student.first_name} {student.last_name}",
        "apogee_code": sid,
        "field_of_study": student.field_of_study,
        "date": today.strftime("%Y-%m-%d"),
        "time": current_time.strftime("%H:%M"),
        "logs_today": len(today_logs) + 1
    }




#to call all student
@router.get("/all_students")
def get_students(db : Session = Depends(get_db)):
    return db.query(Student).all()
@router.get("/all_attendance")
def get_students(db : Session = Depends(get_db)):
    return db.query(Attendance).all()



