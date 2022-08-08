from elasticsearch.helpers import async_bulk
import pytest
import json
from tests.functional.testdata.genres import genres


@pytest.mark.asyncio
async def test_genres_list__genres_present__return_genres(make_get_request, es_client):
    # arrange
    actions = [
        {
            "_index": "genres",
            "_source": json.dumps(genre),
        } for genre in genres
    ]

    await async_bulk(
        client=es_client,
        actions=actions,
        refresh=True
    )

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
async def test_genre_details__genres_present__return_genre(make_get_request, es_client):
    # arrange
    actions = [
        {
            "_index": "genres",
            "_source": json.dumps(genre),
        } for genre in genres
    ]

    await async_bulk(
        client=es_client,
        actions=actions,
        refresh=True
    )

    # act
    response = await make_get_request(
        "/v1/genres/1/",
        # params={"genre_id": "1"}
    )

    # assert
    assert response.body["genres"] == genres[0]
