"""
This file contains the routers for the alert endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.repositories import alert_repo
from src.configs.db_con import SessionLocal
from src.models.schema.alert import ThresholdUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", summary="Get All Alerts")
def get_alerts(db: Session = Depends(get_db)):
    try:
        alerts = alert_repo.get_all_alerts(db)
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#PATCH /api/alerts/{alert_id}
@router.patch("/{medicine_id}")
def update_alert_threshold(medicine_id: int, data: ThresholdUpdate, db: Session = Depends(get_db)):
    alert = alert_repo.update_alert(db, medicine_id, data.new_threshold)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

# DELETE /api/alerts/{alert_id}
@router.delete("/{medicine_id}")
def delete_alert(medicine_id: int, db: Session = Depends(get_db)):
    deleted = alert_repo.delete_alert(db, medicine_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted successfully"}