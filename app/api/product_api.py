from fastapi import APIRouter, Request

from app.api.services import filter_products, search_products

router = APIRouter()


@router.post("/products/filter/")
async def product_filter(request: Request):
    body = await request.json()
    return filter_products(body)
    
@router.get('/product/search/')
async def search_product(search: str):
    return search_products(search)