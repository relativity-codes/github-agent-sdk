import pytest

from github_agent_sdk.pagination import paginate


@pytest.mark.asyncio
async def test_paginate_yields_items_until_short_page() -> None:
    pages = {
        1: [{"id": 1}, {"id": 2}],
        2: [{"id": 3}],
    }

    async def fetcher(page: int, page_size: int):
        assert page_size == 2
        return pages.get(page, [])

    results = [item async for item in paginate(fetcher, page_size=2)]
    assert results == [{"id": 1}, {"id": 2}, {"id": 3}]
