from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID

from app.core.database import get_db
from app.models.customization.customization_group_model import CustomizationGroupModel
from app.models.customization.customization_option_model import CustomizationOptionModel

router = APIRouter(prefix="/customization-groups", tags=["Customization"])


@router.get("/", response_model=List[dict])
async def get_all_customization_groups(session: Session = Depends(get_db)):
    """Obtener todos los grupos de personalización"""
    statement = select(CustomizationGroupModel)
    groups = session.exec(statement).all()
    return [
        {
            "group_id": str(group.group_id),
            "system_name": group.system_name,
            "display_name": group.display_name,
            "created_at": group.created_at.isoformat() if group.created_at else None,
            "updated_at": group.updated_at.isoformat() if group.updated_at else None,
        }
        for group in groups
    ]


@router.post("/", response_model=dict, status_code=201)
async def create_customization_group(
    system_name: str,
    display_name: str,
    session: Session = Depends(get_db),
):
    """Crear un nuevo grupo de personalización"""

    statement = select(CustomizationGroupModel).where(
        CustomizationGroupModel.system_name == system_name
    )
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un grupo con system_name '{system_name}'",
        )

    new_group = CustomizationGroupModel(
        system_name=system_name, display_name=display_name
    )
    session.add(new_group)
    session.commit()
    session.refresh(new_group)

    return {
        "group_id": str(new_group.group_id),
        "system_name": new_group.system_name,
        "display_name": new_group.display_name,
        "created_at": new_group.created_at.isoformat() if new_group.created_at else None,
        "updated_at": new_group.updated_at.isoformat() if new_group.updated_at else None,
    }


@router.get("/{group_id}", response_model=dict)
async def get_customization_group(group_id: UUID, session: Session = Depends(get_db)):
    """Obtener un grupo de personalización por ID"""
    group = session.get(CustomizationGroupModel, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    return {
        "group_id": str(group.group_id),
        "system_name": group.system_name,
        "display_name": group.display_name,
        "created_at": group.created_at.isoformat() if group.created_at else None,
        "updated_at": group.updated_at.isoformat() if group.updated_at else None,
    }


@router.get("/{group_id}/options", response_model=List[dict])
async def get_group_options(group_id: UUID, session: Session = Depends(get_db)):
    """Obtener todas las opciones de un grupo de personalización"""
    group = session.get(CustomizationGroupModel, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    statement = select(CustomizationOptionModel).where(
        CustomizationOptionModel.group_id == group_id
    )
    options = session.exec(statement).all()

    return [
        {
            "option_id": str(option.option_id),
            "group_id": str(option.group_id),
            "name": option.name,
            "extra_cost": float(option.extra_cost),
            "is_size_option": option.is_size_option,
            "details": option.details,
            "consumed_ingredient_id": str(option.consumed_ingredient_id)
            if option.consumed_ingredient_id
            else None,
            "quantity_consumed": float(option.quantity_consumed),
            "created_at": option.created_at.isoformat() if option.created_at else None,
            "updated_at": option.updated_at.isoformat() if option.updated_at else None,
        }
        for option in options
    ]


@router.post("/{group_id}/options", response_model=dict, status_code=201)
async def create_customization_option(
    group_id: UUID,
    name: str,
    extra_cost: float = 0.0,
    is_size_option: bool = False,
    details: str = "",
    consumed_ingredient_id: UUID = None,
    quantity_consumed: float = 0.0,
    session: Session = Depends(get_db),
):
    """Crear una nueva opción de personalización para un grupo"""
    group = session.get(CustomizationGroupModel, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    new_option = CustomizationOptionModel(
        group_id=group_id,
        name=name,
        extra_cost=extra_cost,
        is_size_option=is_size_option,
        details=details,
        consumed_ingredient_id=consumed_ingredient_id,
        quantity_consumed=quantity_consumed,
    )

    session.add(new_option)
    session.commit()
    session.refresh(new_option)

    return {
        "option_id": str(new_option.option_id),
        "group_id": str(new_option.group_id),
        "name": new_option.name,
        "extra_cost": float(new_option.extra_cost),
        "is_size_option": new_option.is_size_option,
        "details": new_option.details,
        "consumed_ingredient_id": str(new_option.consumed_ingredient_id)
        if new_option.consumed_ingredient_id
        else None,
        "quantity_consumed": float(new_option.quantity_consumed),
        "created_at": new_option.created_at.isoformat()
        if new_option.created_at
        else None,
        "updated_at": new_option.updated_at.isoformat()
        if new_option.updated_at
        else None,
    }
