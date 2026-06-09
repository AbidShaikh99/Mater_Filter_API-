from typing import Annotated

from fastapi import APIRouter, Depends
from app.api.services import filter_products_service, search_products_service
from app.schemas.product_schema import ProductFilterRequest, ProductSearchRequest

router = APIRouter()


@router.post("/products/filter/")
async def product_filter(payload: ProductFilterRequest):
    return filter_products_service(payload)


@router.get("/product/search/")
async def search_product(query: Annotated[ProductSearchRequest, Depends()]):
    return search_products_service(query.search)
