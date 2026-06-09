from decimal import Decimal
from pydantic import BaseModel, Field, model_validator

from app.models.product_model import ProductSortField, SortOrder


class ProductFilterRequest(BaseModel):
    brand: str
    status: str | None = None

    min_price: Decimal = Field()
    max_price: Decimal = Field()

    is_featured: bool | None = None
    supplier_country: str | None = None

    sort_by: ProductSortField = ProductSortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC

    page: int = 1
    page_size: int = 20

    @model_validator(mode="after")
    def validate_price_range(self):
        if self.max_price < self.min_price:
            raise ValueError(
                "max_price must be greater than or equal to min_price"
            )
        return self


class ProductSearchRequest(BaseModel):
    search: str = Field(min_length=1)