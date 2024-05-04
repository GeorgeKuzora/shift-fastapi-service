# SHIFT FastAPI service

## Описание

Сервис для сотрудников компании, чтобы они могли проверять свою зарплату и дату следующего повышения.

## Использованные технологии

- Python
- FastAPI
- SQLAlchemy
- Pytest
- Linux
- Docker
- Poetry

## Инструкция по использованию сервиса

### Запуск сервиса в Docker контейнере

#### Описание

Запустить сервис можно используя 2 варианта.

1. Запуск сервиса в режиме разработчика. Он позволяет вносить изменения в код и наблюдать как эти изменения отображаются на работающем сервисе.
2. Запуск сервиса в режиме продакшн. Он отличается меньшим весом контейнера и образа.

#### Подготовка среды для запуска контейнера

Клонируйте репозиторий [shift-fastapi-service](https://gitlab.com/GeorgeKuzora/shift-fastapi-service) в локальную директорию:

Используя https протокол:

```shell
git clone https://gitlab.com/GeorgeKuzora/shift-fastapi-service.git
```

Либо используя SSH протокол:

```shell
git clone git@gitlab.com:GeorgeKuzora/shift-fastapi-service.git
```

Установите Docker на локальный компьютер. Инструкции по установке Docker в вашей операционной системе можно найти на [официальном веб сайте Docker](https://docs.docker.com/get-docker/).

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

#### Сборка контейнера

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

#### Миграция схемы базы данных

Для миграции схемы базы данных отправьте GET запрос на: `https://127.0.0.1:8000/create_schema`

#### Добавление тестового пользователя

Для добавления тестового пользователя отправьте GET запрос на  `https://127.0.0.1:8000/load_data`. Будет создан тестовый пользователь с username: alice и password: alice12345.

#### Авторизация и получение токена

Для авторизации и получения токена для пользователя, сделайте POST запрос с данными в формате form-data: username и password, на адрес  `https://127.0.0.1:8000/load_data`.

#### Получение информации о заплате

Получив токен, направьте GET запрос на адрес   `https://127.0.0.1:8000/salary/me`. Заголовок запроса должен содержать `Authorization: Bearer <полученный токен пользователя>`

#### Получение информации о дате повышения

Получив токен, направьте GET запрос на адрес   `https://127.0.0.1:8000/promotion/me`. Заголовок запроса должен содержать `Authorization: Bearer <полученный токен пользователя>`

### Запуск, перезапуск и остановка контейнера

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

#### Остановка

```shell
docker compose -f docker-compose.dev.yml stop
```
