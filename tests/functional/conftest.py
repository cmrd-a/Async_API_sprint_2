import asyncio
import random
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

import aioredis
import pytest_asyncio
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from faker import Faker
from multidict import CIMultiDictProxy

from models import ElasticMoviesSchemaModel
from settings import settings
from testdata.es_indexes import INDEXES

fake = Faker()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="es_client", scope="session")
async def _es_client():
    client = AsyncElasticsearch(hosts=settings.es_url)
    yield client
    await client.close()


@pytest_asyncio.fixture(name="http_session", scope="session")
async def _http_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(http_session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = f"{settings.service_url}/api{method}"
        async with http_session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest_asyncio.fixture(name="create_indexes", scope="session")
async def _create_indexes(es_client):
    redis = await aioredis.from_url(settings.redis_url)
    await redis.flushall()
    for index, body in INDEXES.items():
        exist = await es_client.indices.exists(index=index)
        if not exist:
            await es_client.indices.create(index=index, **body)

    yield

    for index in INDEXES:
        exist = await es_client.indices.exists(index=index)
        if exist:
            await es_client.indices.delete(index=index)
    await redis.flushall()


def gen_films(qty=100):
    for _ in range(qty):
        doc = ElasticMoviesSchemaModel(
            id=str(uuid4()), imdb_rating=round(random.uniform(0.0, 10.0), 1), title=fake.name()
        )
        yield {
            "_index": "movies",
            "_source": doc.json(),
        }


@pytest_asyncio.fixture(scope="session")
async def create_films(create_indexes, es_client):
    await async_bulk(client=es_client, actions=gen_films(2000), refresh=True)
