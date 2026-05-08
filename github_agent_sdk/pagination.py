from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any


async def paginate(
    fetcher: Callable[[int, int], Awaitable[Any]],
    *,
    page_size: int = 100,
) -> AsyncIterator[dict[str, Any]]:
    page = 1

    while True:
        data = await fetcher(page, page_size)
        items = data if isinstance(data, list) else data.get("items", [])

        if not items:
            break

        for item in items:
            yield item

        if len(items) < page_size:
            break

        page += 1
