import json

import pytest
import pytest_asyncio
from elasticsearch.helpers import async_bulk

from tests.functional.testdata.genres import genres


@pytest_asyncio.fixture(name="save_genres")
async def create_genres(es_client):
    async def inner():
        actions = [
            {
                "_index": "genres",
                "_id": genre["id"],
                "_source": json.dumps(genre),
            }
            for genre in genres
        ]

        await async_bulk(client=es_client, actions=actions, refresh=True)

    return inner


@pytest.mark.asyncio
async def test_genres_list__genres_present__return_genres(make_get_request, save_genres):
    # arrange
    await save_genres()

    # act
    response = await make_get_request("/v1/genres")

    # assert
    assert response.body["genres"] == genres


@pytest.mark.asyncio
async def test_genres_list__no_genres__return_status_404(make_get_request):
    # act
    response = await make_get_request("/v1/genres")

    # assert
    assert response.body["detail"] == "genres not found"
    assert response.status == 404


@pytest.mark.asyncio
async def test_genre_details__genres_present__return_genre(make_get_request, save_genres):
    # arrange
    await save_genres()

    # act
    response = await make_get_request("/v1/genres/1")

    # assert
    assert response.body == genres[0]


@pytest.mark.asyncio
async def test_genre_details__no_genre__return_status_404(make_get_request, save_genres):
    # arrange
    await save_genres()

    # act
    response = await make_get_request("/v1/genres/100")

    # assert
    assert response.body["detail"] == "genre not found"
    assert response.status == 404
