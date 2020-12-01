from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/",
            response_model=List[schemas.User]
            )
async def read_users(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
) -> Any:
    """Get all users.

    Args:
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_superuser).

    Returns:
        Any: [description]
    """
    users = crud.user.get_all(db)
    return users


@router.post("/",
             status_code=201,
             response_model=schemas.User
             )
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_superuser)
) -> Any:
    """Create new user.

    Args:
        user_in (schemas.UserCreate): [description]
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_superuser).

    Returns:
        Any: [description]
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud.user.get_by_name(db, name=user_in.name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/me",
            response_model=schemas.User
            )
async def read_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Get me.

    Args:
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_active_user).

    Returns:
        Any: [description]
    """
    return current_user


@router.put("/me",
            response_model=schemas.User
            )
async def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Update me.

    Args:
        db (Session, optional): [description]. D
        efaults to Depends(deps.get_db).
        password (str, optional): [description].
        Defaults to Body(None).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_active_user).

    Returns:
        Any: [description]
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get user by user id

    Args:
        user_id (int): [description]
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_active_user).
        db (Session, optional): [description]. D
        efaults to Depends(deps.get_db).

    Raises:
        HTTPException: [description]

    Returns:
        Any: [description]
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user_by_id(
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Update user by user id

    Args:
        user_id (int): [description]
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_active_user).
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).

    Returns:
        Any: [description]
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user_by_id(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """DeleteUser

    Args:
        user_id (int): [description]
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_user).
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't delete because current user")
    user = crud.user.remove(db, id=user_id)
    return user
