from typing import Any, Dict, List

from fastapi.responses import JSONResponse

from app.db.database import get_connection

ALLOWED_SORT_FIELDS = {"price", "created_at", "stock_qty"}


def filter_products(body: Dict[str, Any]):
    if not isinstance(body, dict):
        body = {}

    brand = body.get("brand")
    min_price = body.get("min_price")
    max_price = body.get("max_price")
    sort_by = body.get("sort_by", "created_at")
    if sort_by not in ALLOWED_SORT_FIELDS:
        return JSONResponse(
            status_code=400,
            content={"status": False, 
                     "message": "Invalid sort_by value."},
        )

    sort_order = str(body.get("sort_order", "desc")).lower()

    try:
        page = int(body.get("page", 1) or 1)
    except (TypeError, ValueError):
        page = 1

    try:
        page_size = int(body.get("page_size", 20) or 20)
    except (TypeError, ValueError):
        page_size = 20

    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    if page_size > 100:
        return JSONResponse(
            status_code=400,
            content={"status": False, 
                     "message": "page_size is maximum 100"},
        )

    if sort_order not in {"asc", "desc"}:
        sort_order = "desc"

    query_parts = [
        "SELECT *",
        "FROM products",
        "WHERE 1=1",
    ]
    params: List[Any] = []

    if brand is not None and str(brand).strip() != "":
        query_parts.append("AND brand = %s")
        params.append(brand)

    if min_price is not None:
        query_parts.append("AND price >= %s")
        params.append(min_price)

    if max_price is not None:
        query_parts.append("AND price <= %s")
        params.append(max_price)

    query_parts.append(f"ORDER BY {sort_by} {sort_order.upper()}")

    offset = (page - 1) * page_size
    query_parts.append("LIMIT %s OFFSET %s")
    params.extend([page_size, offset])

    query = "\n".join(query_parts)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()

    return {
        "status": True,
        "page": page,
        "page_size": page_size,
        "total": len(result),
        "data": result,
    }


def search_products(search: str):
    query = """
        SELECT *
        FROM products
        WHERE product_name LIKE %s
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (f"%{search}%",))
            result = cursor.fetchall()
        

    return {
        "status": True,
        "total": len(result),
        
        "data": result,
    }
