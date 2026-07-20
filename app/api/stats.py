from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.unit_of_work import UnitOfWork
from app.api.schema.stats import StatsResponse
from app.services.stats_service import StatsService

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)

def get_stats_service(
    db: Session = Depends(get_db),
):
    return StatsService(UnitOfWork(db))


@router.get(
    "",
    response_model=StatsResponse,
    summary="Dashboard statistics",
)
def get_stats(
    service: StatsService = Depends(
        get_stats_service
    ),
):
    return service.get_stats()