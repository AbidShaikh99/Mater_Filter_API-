from typing import Any, Dict, List

from app.db.database import get_connection


def filter_products_query(payload) -> Dict[str, Any]:

    query_parts = [
        "SELECT *",
        "FROM products",
        "WHERE 1=1"
    ]

    count_query_parts = [
        "SELECT COUNT(*) AS total",
        "FROM products",
        "WHERE 1=1"
    ]

    params: List[Any] = []
    count_params: List[Any] = []

    if payload.brand:
        query_parts.append("AND brand = %s")
        count_query_parts.append("AND brand = %s")

        params.append(payload.brand)
        count_params.append(payload.brand)

    if payload.status:
        query_parts.append("AND status = %s")
        count_query_parts.append("AND status = %s")

        params.append(payload.status)
        count_params.append(payload.status)

    if payload.min_price is not None:
        query_parts.append("AND price >= %s")
        count_query_parts.append("AND price >= %s")

        params.append(payload.min_price)
        count_params.append(payload.min_price)

    if payload.max_price is not None:
        query_parts.append("AND price <= %s")
        count_query_parts.append("AND price <= %s")

        params.append(payload.max_price)
        count_params.append(payload.max_price)

    if payload.is_featured is not None:
        query_parts.append("AND is_featured = %s")
        count_query_parts.append("AND is_featured = %s")

        params.append(payload.is_featured)
        count_params.append(payload.is_featured)

    if payload.supplier_country:
        query_parts.append(
            "AND supplier_country = %s"
        )
        count_query_parts.append(
            "AND supplier_country = %s"
        )

        params.append(payload.supplier_country)
        count_params.append(payload.supplier_country)

    query_parts.append(
        f"ORDER BY {payload.sort_by.value} "
        f"{payload.sort_order.value.upper()}"
    )

    offset = (
        (payload.page - 1)
        * payload.page_size
    )

    query_parts.append(
        "LIMIT %s OFFSET %s"
    )

    params.extend([
        payload.page_size,
        offset
    ])

    query = "\n".join(query_parts)

    count_query = "\n".join(
        count_query_parts
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                count_query,
                count_params
            )

            total = cursor.fetchone()["total"]

            cursor.execute(
                query,
                params
            )

            products = cursor.fetchall()

    return {
        "products": products,
        "total": total
    }


def search_products_query(search: str):

    query = """
    SELECT *
    FROM products
    WHERE product_name LIKE %s
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (f"%{search}%",)
            )

            products = cursor.fetchall()
        return products
