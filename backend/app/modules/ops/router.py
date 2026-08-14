from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.ops.service import OpsService
from app.modules.ops.schemas import OpsOverviewResponse

router = APIRouter(tags=["ops"])


@router.get("/ops/overview", response_model=OpsOverviewResponse, summary="Get operational & business metrics overview")
@router.get("/admin/overview", response_model=OpsOverviewResponse, summary="Get operational & business metrics overview")
def get_ops_overview(db: Session = Depends(get_db)):
    """
    Returns aggregated operational and business telemetry metrics
    including active users, request counts, exercise accuracy, and system health.
    """
    svc = OpsService(db)
    return svc.get_overview()
