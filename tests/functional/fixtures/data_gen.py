import json

import pytest_asyncio
from elasticsearch.helpers import async_bulk
from utils.data_gen import gen_films

from tests.functional.testdata.genres import genres


@pytest_asyncio.fixture()
async def create_films(es_client):
    async def inner(quantity=1000):
        return await async_bulk(client=es_client, actions=gen_films(quantity), refresh=True)

    return inner


@pytest_asyncio.fixture()
async def create_genres(es_client):
    actions = [
        {
            "_index": "genres",
            "_id": genre["id"],
            "_source": json.dumps(genre),
        }
        for genre in genres
    ]

    await async_bulk(client=es_client, actions=actions, refresh=True)
