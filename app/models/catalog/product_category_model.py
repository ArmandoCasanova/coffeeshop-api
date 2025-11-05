from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class ProductCategoryModel(SQLModel, table=True):
    __tablename__ = "product_categories"
    
    category_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    image_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
