import pymysql

from app.repositories.product_repository import filter_products_query, search_products_query
from app.schemas.product_schema import ProductFilterRequest
from app.utils.response import ResponseUtil


def filter_products_service(payload: ProductFilterRequest):
    # if (
    #     payload.min_price is not None
    #     and payload.max_price is not None
    #     and payload.min_price > payload.max_price
    # ):
    #     return ResponseUtil.error(
    #         "Min price cannot be greater than max price."
    #     )

    try:
        result = filter_products_query(payload)
    except pymysql.MySQLError:
        return ResponseUtil.error(
            "Unable to fetch products.",
            status_code=400
        )

    return ResponseUtil.success(
        data=result["products"],
        total=result["total"],
        page=payload.page,
        page_size=payload.page_size
    )


def search_products_service(search: str):
    if not search.strip():
        return ResponseUtil.error(
            "Search text is required."
        )

    try:
        products = search_products_query(search)
    except pymysql.MySQLError:
        return ResponseUtil.error(
            "Unable to search products.",
            status_code=400
        )

    return ResponseUtil.success(
        data=products,
        total=len(products)
    )
