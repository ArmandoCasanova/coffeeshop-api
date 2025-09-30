from .product_model import ProductModel
from .product_category_model import ProductCategoryModel
from .product_category_link_model import ProductCategoryLinkModel

ProductModel.model_rebuild()
ProductCategoryModel.model_rebuild()
ProductCategoryLinkModel.model_rebuild()
