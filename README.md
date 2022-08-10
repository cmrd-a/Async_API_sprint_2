# Проектная работа 5 спринта, команда 19

https://github.com/cmrd-a/Async_API_sprint_2

## Проект "Фильмотека"
Состоит из:
 - API для поиска информации о фильмах, жанрах и актёрах.
 - Админка для создания, изменения и удаления вышеобозначенных объектов.

### Запуск сервисов:
 1. `cp .env.example .env`
 2. `make prod_up`

API доступно по адресу: http://localhost/api/openapi.

А админка по http://localhost/admin/. Логин и пароль 'admin'.

### Запуск тестов:
 1. `cp tests/functional/.env.example tests/functional/.env`
 2. `make tests_up`

### Команды для разработки:
 - `make dev_up` - поднять только БД с открытыми портами.
 - `make black` - отформатировать код.

---
@cmrd-a - тимлид

@nu-kotov - разработчик