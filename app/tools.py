from __future__ import annotations

import asyncio

from agents import function_tool


@function_tool
async def create_user(name: str, phone: str, email: str | None = None) -> dict[str, str]:
    """Create a customer profile.

    Args:
        name: Customer full name.
        phone: Customer phone number.
        email: Optional customer email address.
    """
    await asyncio.sleep(1)
    return {
        "user_id": "usr_dummy_001",
        "name": name,
        "phone": phone,
        "email": email or "",
        "status": "created",
    }


@function_tool
async def search_user(phone: str | None = None, email: str | None = None) -> list[dict[str, str]]:
    """Search for existing customers.

    Args:
        phone: Customer phone number.
        email: Customer email address.
    """
    await asyncio.sleep(1)
    if not phone and not email:
        return []

    return [
        {
            "user_id": "usr_dummy_001",
            "name": "Demo Customer",
            "phone": phone or "+359000000000",
            "email": email or "demo@example.com",
        }
    ]


@function_tool
async def search_flowers(
    query: str,
    occasion: str | None = None,
    max_price: float | None = None,
) -> list[dict[str, str | float]]:
    """Search available flowers and arrangements.

    Args:
        query: Flower, bouquet, color, or style requested by the customer.
        occasion: Optional occasion such as birthday, anniversary, or apology.
        max_price: Optional maximum price the customer wants to spend.
    """
    await asyncio.sleep(1)
    return [
        {
            "flower_id": "flw_roses_12",
            "name": "Classic Red Roses",
            "description": "A dozen red roses with seasonal greenery.",
            "price": 59.0,
            "occasion": occasion or "romantic",
        },
        {
            "flower_id": "flw_spring_mix",
            "name": "Spring Garden Bouquet",
            "description": "Mixed tulips, ranunculus, and fresh greenery.",
            "price": 45.0 if max_price is None or max_price >= 45.0 else max_price,
            "occasion": occasion or "celebration",
        },
    ]


@function_tool
async def create_order(
    user_id: str,
    flower_id: str,
    quantity: int,
    recipient_name: str,
    delivery_address: str,
    delivery_date: str,
    note: str | None = None,
) -> dict[str, str | int]:
    """Create a flower order.

    Args:
        user_id: Customer identifier.
        flower_id: Selected flower or arrangement identifier.
        quantity: Number of arrangements.
        recipient_name: Delivery recipient name.
        delivery_address: Full delivery address.
        delivery_date: Requested delivery date.
        note: Optional card or delivery note.
    """
    await asyncio.sleep(1)
    return {
        "order_id": "ord_dummy_001",
        "user_id": user_id,
        "flower_id": flower_id,
        "quantity": quantity,
        "recipient_name": recipient_name,
        "delivery_address": delivery_address,
        "delivery_date": delivery_date,
        "note": note or "",
        "status": "created",
    }


FLOWER_ORDER_TOOLS = [create_user, search_user, search_flowers, create_order]
