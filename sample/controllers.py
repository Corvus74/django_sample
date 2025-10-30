from fastapi import APIRouter, Depends
from typing import List

from .dependencies import get_api_service
from api.dependencies import get_replacement_part_service
from .services.apiservices import ApiService
from api.services import ReplacementPartService
from api.schemas import ReplacementPart # Corrected import

router = APIRouter()


@router.get("/sample-data")
def get_sample_data(
    api_service: ApiService = Depends(get_api_service),
):
    return api_service.get_data()


@router.get("/replacement-parts-page", response_model=List[ReplacementPart])
def get_replacement_parts_page(
    part_service: ReplacementPartService = Depends(get_replacement_part_service),
):
    return part_service.get_replacement_parts()
