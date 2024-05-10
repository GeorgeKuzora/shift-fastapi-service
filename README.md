# SHIFT FastAPI service

## Описание

Сервис для сотрудников компании, чтобы они могли проверять свою зарплату и дату следующего повышения.

## Использованные технологии

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Pytest
- Linux
- Poetry
- Docker

## Инструкция по использованию сервиса

### Запуск сервиса

#### Описание

Запустить сервис можно используя 3 варианта.

1. Запуск сервиса в виртуальном окружении Python созданном при помощи Poetry.
2. Запуск сервиса в Docker контейнере в режиме разработчика. Он позволяет вносить изменения в код и наблюдать как эти изменения отображаются на работающем сервисе.
3. Запуск сервиса в Docker контейнере в режиме продакшн. Он отличается меньшим весом контейнера и образа и сохраняет данные в именованном томе Docker.

#### Подготовка среды для запуска сервиса

Клонируйте репозиторий [shift-fastapi-service](https://gitlab.com/GeorgeKuzora/shift-fastapi-service) в локальную директорию:

Используя https протокол:

```shell
git clone https://gitlab.com/GeorgeKuzora/shift-fastapi-service.git
```

Либо используя SSH протокол:

```shell
git clone git@gitlab.com:GeorgeKuzora/shift-fastapi-service.git
```

Если вы хотите запустить сервис в виртуальном окружении, установите Python версии 3.12.2 или выше и Poetry на локальный компьютер. Инструкции по установке Python и Poetry на вашей операционной системе вы можете найти на официальных сайтах: [Официальный сайт Python](https://www.python.org/downloads/), [Официальный сайт Poetry](https://python-poetry.org/docs/#installation).

Если вы хотите запустить сервис в Docker контейнере, установите Docker на локальный компьютер. Инструкции по установке Docker в вашей операционной системе можно найти на [официальном веб сайте Docker](https://docs.docker.com/get-docker/).

Создайте файл `.env`.

Для этого скопируйте файл `.env.template` в файл `.env`.

В Linux и MacOS:

```shell
cp .env.template .env
```

В Windows:

```powershell
Copy-Item -Path <Путь к .env.template> -Destination <Путь к .env>
```

Выполните команду:

```shell
openssl rand -hex 32
```

Она сгенерирует ключ. Присвойте этот ключ переменной `SECRET_KEY` в файле `.env`:

```shell
SECRET_KEY=<Скопируйте свой ключ сюда>
```

#### Запуск в виртуальном окружении

Перейдите в корневую директорию проекта, там где расположен файл `pyproject.toml`.

Выполните команду создания виртуального окружения и установки проекта в него:

```shell
poetry install
```

Для запуска сервера с сервисом выполните команду:

```shell
poetry run uvicorn shift_fastapi_service.main:app --host 0.0.0.0 --port 8000 --reload
```

Сервер будет работать по ссылке: `https://127.0.0.1:8000`.

#### Запуск в контейнере

Для того чтобы собрать и запустить контейнер выполните следующую команду docker-compose:

Для контейнера в режиме разработки:

```shell
docker compose -f docker-compose.dev.yml up -d
```

Для контейнера в режиме продакшн:

```shell
docker compose -f docker-compose.prod.yml up -d
```

Сервер будет работать по ссылке: `https://127.0.0.1:8000`.

### Работа с сервисом

#### Миграция схемы базы данных

Для миграции схемы базы данных отправьте GET запрос на: `https://127.0.0.1:8000/create_schema`

#### Добавление тестового пользователя

Для добавления тестового пользователя отправьте GET запрос на  `https://127.0.0.1:8000/load_data`. Будет создан тестовый пользователь с username: alice и password: alice12345.

#### Создание пользователя

Для добавления своего пользователя отправьте POST запрос на  `https://127.0.0.1:8000/create_user`.
Тело запроса должно содержать следующие поля:

- username
- email
- salary
- next_promotion_date
- password

Будет создан пользователь в базе данных.

#### Авторизация и получение токена

Для авторизации и получения токена для пользователя, сделайте POST запрос с данными в формате form-data: username и password, на адрес  `https://127.0.0.1:8000/token`.

#### Получение информации о заплате

Получив токен, направьте GET запрос на адрес   `https://127.0.0.1:8000/salary/me`. Заголовок запроса должен содержать `Authorization: Bearer <полученный токен пользователя>`

#### Получение информации о дате повышения

Получив токен, направьте GET запрос на адрес   `https://127.0.0.1:8000/promotion/me`. Заголовок запроса должен содержать `Authorization: Bearer <полученный токен пользователя>`

### Запуск, перезапуск и остановка контейнера с сервисом

Для запуска, перезапуска и остановки контейнера рекомендуется использовать команды Docker Compose:

#### Запуск

```shell
docker compose -f docker-compose.dev.yml start
```

```shell
docker compose -f docker-compose.prod.yml start
```

#### Перезапуск

```shell
docker compose -f docker-compose.dev.yml restart
```

```shell
docker compose -f docker-compose.prod.yml restart
```

#### Остановка

```shell
docker compose -f docker-compose.dev.yml stop
```

```shell
docker compose -f docker-compose.prod.yml stop
```
