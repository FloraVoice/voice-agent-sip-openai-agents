from __future__ import annotations

import asyncio
import os
from urllib.parse import quote

import aiohttp
from agents import function_tool


FLORA_API_BASE_URL = os.getenv("FLORA_API_BASE_URL", "http://localhost:8001").rstrip("/")


async def _get_json(path: str) -> object:
    url = f"{FLORA_API_BASE_URL}{path}"
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers={"Accept": "application/json"}) as response:
                if response.status >= 400:
                    detail = await response.text()
                    raise RuntimeError(f"Flora API returned {response.status}: {detail}")

                return await response.json()
    except aiohttp.ClientError as exc:
        raise RuntimeError(f"Could not reach Flora API at {url}: {exc}") from exc


async def _post_json(path: str, payload: dict[str, object]) -> object:
    url = f"{FLORA_API_BASE_URL}{path}"
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                url,
                json=payload,
                headers={"Accept": "application/json"},
            ) as response:
                if response.status >= 400:
                    detail = await response.text()
                    raise RuntimeError(f"Flora API returned {response.status}: {detail}")

                return await response.json()
    except aiohttp.ClientError as exc:
        raise RuntimeError(f"Could not reach Flora API at {url}: {exc}") from exc


@function_tool
async def create_user(
    username: str,
    phone_number: str,
    address: str,
    email: str,
) -> dict[str, str]:
    """Create a customer profile.

    Args:
        username: Customer full name or preferred display name.
        phone_number: Customer phone number.
        address: Customer delivery address.
        email: Customer email address.
    """
    user = await _post_json(
        "/users/",
        {
            "email": email,
            "username": username,
            "phone_number": phone_number,
            "address": address,
        },
    )
    if not isinstance(user, dict):
        raise RuntimeError("Flora API returned an unexpected user response.")

    return user


@function_tool
async def search_user(
    phone_number: str | None = None,
    email: str | None = None,
) -> list[dict[str, str]]:
    """Search for existing customers.

    Args:
        phone_number: Customer phone number.
        email: Customer email address.
    """
    query = phone_number or email
    if not query:
        return []

    users = await _get_json(f"/users/search?q={quote(query)}&limit=5")
    if not isinstance(users, list):
        raise RuntimeError("Flora API returned an unexpected users response.")

    return users


@function_tool
async def get_all_flowers() -> list[dict[str, str | float | int]]:
    """Get every available flower from the Flora API."""
    flowers = await _get_json("/flowers/")
    if not isinstance(flowers, list):
        raise RuntimeError("Flora API returned an unexpected flowers response.")

    return flowers


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


FLOWER_ORDER_TOOLS = [create_user, search_user, get_all_flowers, search_flowers, create_order]
