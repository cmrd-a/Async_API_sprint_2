import time

from elasticsearch import Elasticsearch

from settings import settings


def wait_es():
    client = Elasticsearch(hosts=settings.es_url)
    while not client.ping():
        time.sleep(2)


if __name__ == "__main__":
    wait_es()
