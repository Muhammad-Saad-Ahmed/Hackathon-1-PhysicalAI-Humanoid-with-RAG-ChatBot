from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...database.repositories import SavedGenerationParameterSetRepository
from ...models.generation_params import SavedGenerationParameterSet, SavedGenerationParameterSetCreate, SavedGenerationParameterSetUpdate
from ...models.textbook_generation import GenerateTextbookRequest

router = APIRouter()

@router.post("/", response_model=SavedGenerationParameterSet)
def save_parameter_set(
    saved_set_create: SavedGenerationParameterSetCreate,
    db: Session = Depends(get_db)
):
    """
    Save a new set of generation parameters.
    """
    # Check if a set with the same name already exists
    existing_set = SavedGenerationParameterSetRepository.get_by_name(db, saved_set_create.name)
    if existing_set:
        raise HTTPException(status_code=400, detail="Parameter set with this name already exists.")

    return SavedGenerationParameterSetRepository.create(db, saved_set_create)


@router.get("/{set_id}", response_model=SavedGenerationParameterSet)
def get_parameter_set_by_id(
    set_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a saved set of generation parameters by its ID.
    """
    saved_set = SavedGenerationParameterSetRepository.get(db, set_id)
    if not saved_set:
        raise HTTPException(status_code=404, detail="Parameter set not found.")
    return saved_set

@router.get("/name/{set_name}", response_model=SavedGenerationParameterSet)
def get_parameter_set_by_name(
    set_name: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a saved set of generation parameters by its name.
    """
    saved_set = SavedGenerationParameterSetRepository.get_by_name(db, set_name)
    if not saved_set:
        raise HTTPException(status_code=404, detail="Parameter set not found.")
    return saved_set

@router.get("/", response_model=List[SavedGenerationParameterSet])
def list_parameter_sets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all saved generation parameter sets.
    """
    return SavedGenerationParameterSetRepository.get_all(db, skip=skip, limit=limit)
