from typing import Optional, List
from uuid import UUID
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, Query, Form, File, UploadFile, HTTPException
from sqlmodel import Session
from fastapi.concurrency import run_in_threadpool
import aiofiles

from app.core.database import get_db 
from app.api.categories.category_controller import CategoryController
from app.api.categories.category_schema import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
    CategoryListResponseSchema,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_controller(session: Session = Depends(get_db)) -> CategoryController:
    return CategoryController(session)


async def save_category_image(image: UploadFile) -> str:
    """Guarda el archivo subido en el directorio estático y devuelve su URL relativa."""
    
    UPLOAD_DIR = Path("static/images/categories")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 

    file_extension = Path(image.filename or "").suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await image.read(65536):
                await out_file.write(content)
        
        
        return f"/static/images/categories/{unique_filename}"
        
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        
        raise HTTPException(
            status_code=500, detail="Error al procesar y guardar la imagen de la categoría."
        )


@router.post(
    "",
    response_model=CategoryResponseSchema,
    status_code=201,
    summary="Crear una nueva categoría con imagen (multipart/form-data)"
)
async def create_category(
    
    name: str = Form(...),
    description: Optional[str] = Form(None),
    
    image: Optional[UploadFile] = File(None),
    controller: CategoryController = Depends(get_category_controller),
):
    """Crea una nueva categoría. Si se proporciona una imagen, la guarda."""
    
    image_url: Optional[str] = None
    
    if image and image.filename:
        
        image_url = await save_category_image(image)
    
   
    category_data = CategoryCreateSchema(
        name=name,
        description=description,
        image_url=image_url 
    )


    return await run_in_threadpool(controller.create_category, category_data)


@router.get("", response_model=CategoryListResponseSchema)
async def get_all_categories(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    controller: CategoryController = Depends(get_category_controller),
):
    """Obtener todas las categorías con paginación"""
    return await run_in_threadpool(controller.get_all_categories, page, page_size)


@router.get("/search", response_model=CategoryListResponseSchema)
async def search_categories(
    name: str = Query(..., min_length=1, description="Category name to search"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    controller: CategoryController = Depends(get_category_controller),
):
    """Buscar categorías por nombre"""
    return await run_in_threadpool(controller.search_categories, name, page, page_size)


@router.get("/{category_id}", response_model=CategoryResponseSchema)
async def get_category(
    category_id: UUID, controller: CategoryController = Depends(get_category_controller)
):
    """Obtener una categoría por ID"""
    return await run_in_threadpool(controller.get_category, category_id)


@router.put(
    "/{category_id}",
    response_model=CategoryResponseSchema,
    summary="Actualizar una categoría por ID (multipart/form-data)"
)
async def update_category(
    category_id: UUID,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    controller: CategoryController = Depends(get_category_controller),
):
    """Actualiza una categoría, esperando 'multipart/form-data' del frontend."""
    
    update_data = {}
    image_url: Optional[str] = None

   
    if image and image.filename:
        image_url = await save_category_image(image)
        update_data["image_url"] = image_url

    
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
        
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar.")

    
    category_data = CategoryUpdateSchema(**update_data)
    
    
    return await run_in_threadpool(
        controller.update_category, category_id, category_data
    )

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID, controller: CategoryController = Depends(get_category_controller)
):
    """Eliminar una categoría"""
    
    return await run_in_threadpool(controller.delete_category, category_id)


@router.post(
    "/json",
    response_model=CategoryResponseSchema,
    status_code=201,
    summary="Crear una nueva categoría con JSON (image_url desde Cloudinary)"
)
async def create_category_json(
    category_data: CategoryCreateSchema,
    controller: CategoryController = Depends(get_category_controller),
):
    """
    Crea una nueva categoría recibiendo JSON con image_url (para imágenes en Cloudinary).
    Este endpoint es para la app móvil que sube imágenes a Cloudinary externamente.
    """
    return await run_in_threadpool(controller.create_category, category_data)

@router.put(
    "/{category_id}/json",
    response_model=CategoryResponseSchema,
    summary="Actualizar una categoría con JSON (image_url desde Cloudinary)"
)
async def update_category_json(
    category_id: UUID,
    category_data: CategoryUpdateSchema,
    controller: CategoryController = Depends(get_category_controller),
):
    """
    Actualiza una categoría recibiendo JSON con image_url (para imágenes en Cloudinary).
    Este endpoint es para la app móvil que sube imágenes a Cloudinary externamente.
    """
    return await run_in_threadpool(
        controller.update_category, category_id, category_data
    )
