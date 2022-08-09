import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("page_size", (1, 2, 50, 99))
async def test_films_list__page_size_parameter__return_correct_result(create_films, make_get_request, page_size):
    # arrange
    await create_films(100)

    # act
    response = await make_get_request("/v1/films", {"page[size]": page_size})

    # assert
    assert response.status == 200
    assert len(response.body["results"]) == page_size


@pytest.mark.asyncio
async def test_films_list__sort_by_rating__return_correct_films(create_movies, make_get_request):
    # arrange
    expected_result = {
        "total": 6,
        "results": [
            {"id": "1", "title": "Test film 1 title", "imdb_rating": 1.5},
            {"id": "2", "title": "Test film 2 title", "imdb_rating": 3.5},
            {"id": "3", "title": "Test film 3 title", "imdb_rating": 5.5},
            {"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5},
            {"id": "5", "title": "Test film 5 title", "imdb_rating": 7.5},
            {"id": "6", "title": "Original name", "imdb_rating": 8.5},
        ],
    }

    # act
    response = await make_get_request("/v1/films", {"sort": "imdb"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_list__filter_by_genre__return_correct_films(create_movies, make_get_request):
    # arrange
    expected_result = {"total": 1, "results": [{"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5}]}

    # act
    response = await make_get_request("/v1/films", {"filter[genre]": "4"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_list__filter_by_person__return_correct_films(create_movies, make_get_request):
    # arrange
    expected_result = {"total": 1, "results": [{"id": "2", "title": "Test film 2 title", "imdb_rating": 3.5}]}

    # act
    response = await make_get_request("/v1/films", {"filter[person]": "10"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_list__no_films__return_status_404(make_get_request):
    # act
    response = await make_get_request("/v1/films")

    # assert
    assert response.body["detail"] == "films not found"
    assert response.status == 404


@pytest.mark.asyncio
async def test_films_search__search_by_title__return_correct_films(create_movies, make_get_request):
    # arrange
    expected_result = {"total": 1, "results": [{"id": "6", "title": "Original name", "imdb_rating": 8.5}]}

    # act
    response = await make_get_request("/v1/films/search", {"query": "original"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_search__no_films__return_status_404(create_movies, make_get_request):
    # act
    response = await make_get_request("/v1/films/search", {"query": "korpiklaani"})

    # assert
    assert response.body["detail"] == "films not found"
    assert response.status == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("page_size", (1, 2, 3))
async def test_films_search__send_page_size__return_correct_lens(make_get_request, create_movies, page_size):
    response = await make_get_request(
        "/v1/films/search",
        {"query": "test", "page[size]": page_size},
    )

    assert response.status == 200
    assert len(response.body["results"]) == page_size


@pytest.mark.asyncio
async def test_film_details__search_by_title__return_correct_film(create_movies, make_get_request):
    # arrange
    expected_result = {
        "id": "1",
        "title": "Test film 1 title",
        "imdb_rating": 1.5,
        "description": "test description",
        "genres": [{"id": "1", "name": "action"}],
        "actors": [
            {"id": "1", "name": "Pablo Escobar"},
            {"id": "2", "name": "Victor Andrey"},
            {"id": "9", "name": "Igor Rastvorov"},
        ],
        "writers": [{"id": "11", "name": "Igor Presnyakov"}],
        "directors": [],
    }

    # act
    response = await make_get_request("/v1/films/1")

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_film_details__no_film__return_status_404(create_movies, make_get_request):
    # act
    response = await make_get_request("/v1/films/100")

    # assert
    assert response.body["detail"] == "film not found"
    assert response.status == 404
