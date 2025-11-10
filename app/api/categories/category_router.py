from typing import Optional, List
from uuid import UUID
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, Query, Form, File, UploadFile, HTTPException
from sqlmodel import Session
from fastapi.concurrency import run_in_threadpool
import aiofiles

# Asegúrate de que las rutas de importación siguientes sean correctas para tu estructura de proyecto:
from app.core.database import get_db 
from app.api.categories.category_controller import CategoryController
from app.api.categories.category_schema import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
    CategoryListResponseSchema,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

# --- Dependencia para obtener el Controller ---
def get_category_controller(session: Session = Depends(get_db)) -> CategoryController:
    return CategoryController(session)
# ---------------------------------------------


# 🌟 FUNCIÓN CLAVE PARA GUARDAR EL ARCHIVO 🌟
async def save_category_image(image: UploadFile) -> str:
    """Guarda el archivo subido en el directorio estático y devuelve su URL relativa."""
    
    # Define el directorio de guardado: 'static/images/categories'
    UPLOAD_DIR = Path("static/images/categories")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True) # Asegura que el directorio exista

    # Genera un nombre de archivo único usando UUID
    file_extension = Path(image.filename or "").suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Lógica de guardado asíncrono
    try:
        # Escribe el archivo en el disco en chunks (64KB)
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await image.read(65536):
                await out_file.write(content)
        
        # URL relativa que se guardará en la base de datos y usará el frontend
        return f"/static/images/categories/{unique_filename}"
        
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        # Lanza una excepción HTTP si falla el guardado
        raise HTTPException(
            status_code=500, detail="Error al procesar y guardar la imagen de la categoría."
        )


# ----------------------------------------------------------------------
# 📌 1. Crear Categoría (POST /)
@router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=201,
    summary="Crear una nueva categoría con imagen (multipart/form-data)"
)
async def create_category(
    # Recibimos los campos de texto como Form
    name: str = Form(...),
    description: Optional[str] = Form(None),
    # Recibimos la imagen con File
    image: Optional[UploadFile] = File(None),
    controller: CategoryController = Depends(get_category_controller),
):
    """Crea una nueva categoría. Si se proporciona una imagen, la guarda."""
    
    image_url: Optional[str] = None
    
    if image and image.filename:
        # Llama a la función de guardado real
        image_url = await save_category_image(image)
    
    # Crea el esquema con la URL de la imagen
    category_data = CategoryCreateSchema(
        name=name,
        description=description,
        image_url=image_url 
    )

    # Llama al Controller (Síncrono) en el Threadpool
    return await run_in_threadpool(controller.create_category, category_data)


# ----------------------------------------------------------------------

# 📌 2. Listar Categorías (GET /)
@router.get("/", response_model=CategoryListResponseSchema)
async def get_all_categories(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    controller: CategoryController = Depends(get_category_controller),
):
    """Obtener todas las categorías con paginación"""
    return await run_in_threadpool(controller.get_all_categories, page, page_size)


# 📌 3. Buscar Categorías (GET /search)
@router.get("/search", response_model=CategoryListResponseSchema)
async def search_categories(
    name: str = Query(..., min_length=1, description="Category name to search"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    controller: CategoryController = Depends(get_category_controller),
):
    """Buscar categorías por nombre"""
    return await run_in_threadpool(controller.search_categories, name, page, page_size)


# 📌 4. Obtener Categoría por ID (GET /{category_id})
@router.get("/{category_id}", response_model=CategoryResponseSchema)
async def get_category(
    category_id: UUID, controller: CategoryController = Depends(get_category_controller)
):
    """Obtener una categoría por ID"""
    return await run_in_threadpool(controller.get_category, category_id)


# 📌 5. Actualizar Categoría (PUT /{category_id})
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

    # Procesa y guarda la nueva imagen si fue enviada
    if image and image.filename:
        image_url = await save_category_image(image)
        update_data["image_url"] = image_url

    # Agrega campos de texto si fueron enviados
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
        
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar.")

    # Crea el esquema de actualización con los datos recibidos (incluida la nueva URL de la imagen)
    category_data = CategoryUpdateSchema(**update_data)
    
    # Llama al Controller para la actualización en la BD
    return await run_in_threadpool(
        controller.update_category, category_id, category_data
    )

# 📌 6. Eliminar Categoría (DELETE /{category_id})
@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID, controller: CategoryController = Depends(get_category_controller)
):
    """Eliminar una categoría"""
    # Nota: Aquí deberías añadir lógica para eliminar el archivo físico de la imagen si existe.
    return await run_in_threadpool(controller.delete_category, category_id)
