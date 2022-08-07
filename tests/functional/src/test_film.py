import pytest


class TestV1FilmsListHandler:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("page_size", (1, 2, 50, 99))
    async def test_film(self, create_films, make_get_request, page_size):
        await create_films(100)
        response = await make_get_request("/v1/films", {"page[size]": page_size})

        assert response.status == 200
        assert len(response.body["results"]) == page_size
