from enum import Enum

class ProductSortField(str, Enum):
    PRICE = "price"
    CREATED_AT = "created_at"
    STOCK_QTY = "stock_qty"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"