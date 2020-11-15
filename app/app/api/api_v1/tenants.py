from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/",
            responce_model=List[schemas.Tenant]
            )
async def read_tenants(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_super_user)
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
    tenants = crud.tenants.get_all(db)
    return tenants


@router.get("/{tenant_id}",
            response_model=schemas.Tenant
            )
async def read_tenant_by_id(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: int,
    current_user: models.User = Depends(deps.get_current_super_user)
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
    tenant = crud.tenant.get(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Item not found")
    return tenant


@router.post("/",
             responce_model=schemas.Tenant
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
    tenant = crud.tenant.create(db, tenant_in)
    return tenant


@router.put("/{tenant_id}",
            responce_model=schemas.Tenant
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
    tenant = crud.tenant.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    tenant = crud.tenant.update(db, db_obj=tenant, obj_in=tenant_in)
    return tenant


@router.delete("/{tenant_id}",
               respoce_model=schemas.Tenant
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
    tenant = crud.tenant.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    tenant = crud.tenant.remove(db, id=tenant_id)
    return tenant
