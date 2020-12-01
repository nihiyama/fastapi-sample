from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/",
            response_model=List[schemas.Tenant]
            )
async def read_tenants(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser)
) -> Any:
    """Get tennants.

    Args:
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_user).

    Returns:
        Any: [description]
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user doesn't have enough privileges")
    tenants = crud.tenant.get_all(db)
    return tenants


@router.get("/{tenant_id}",
            response_model=schemas.Tenant
            )
async def read_tenant_by_id(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
) -> Any:
    """Get tenant by id.

    Args:
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_super_user).

    Returns:
        Any: [description]
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user doesn't have enough privileges")
    tenant = crud.tenant.get(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found")
    return tenant


@router.post("/",
             status_code=201,
             response_model=schemas.Tenant
             )
async def create_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_in: schemas.TenantCreate,
    current_user: models.User = Depends(deps.get_current_superuser)
) -> Any:
    """Create tenant

    Args:
        tenant_in (schemas.TenantCreate): [description]
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_superuser).

    Returns:
        Any: [description]
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user doesn't have enough privileges")
    tenant = crud.tenant.create(db, obj_in=tenant_in)
    return tenant


@router.put("/{tenant_id}",
            response_model=schemas.Tenant
            )
async def update_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: int,
    tenant_in: schemas.TenantUpdate,
    current_user: models.User = Depends(deps.get_current_superuser)
) -> Any:
    """Update tenants

    Args:
        tenant_id (int): [description]
        tenant_in (schemas.TenantUpdate): [description]
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_superuser).

    Returns:
        Any: [description]
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user doesn't have enough privileges")
    tenant = crud.tenant.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found")
    tenant = crud.tenant.update(db, db_obj=tenant, obj_in=tenant_in)
    return tenant


@router.delete("/{tenant_id}",
               response_model=schemas.Tenant
               )
async def delete_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
) -> Any:
    """Delete tenant.

    Args:
        tenant_id (int): [description]
        db (Session, optional): [description].
        Defaults to Depends(deps.get_db).
        current_user (models.User, optional): [description].
        Defaults to Depends(deps.get_current_superuser).

    Returns:
        Any: [description]
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user doesn't have enough privileges")
    tenant = crud.tenant.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found")
    tenant = crud.tenant.remove(db, id=tenant_id)
    return tenant
