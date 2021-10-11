from enum import Enum


class EnumStatusOrder(Enum):
    CONFIRMED = 0
    PAID_UP = 1


class MockOrder:
    """
    Required fields which you must have in the Order model.
    """
    pk = 1
    status = EnumStatusOrder.CONFIRMED.value
    total_price = 888
