# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```python
# команды создания виртуального окружения
# и установки необходимых библиотек в него
cd services
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# команда перехода в директорию
cd ml_service

# команда запуска сервиса с помощью uvicorn
uvicorn main:app --host 0.0.0.0 --port 1702
```

### Пример curl-запроса к микросервису

```bash
curl -X POST "http://127.0.0.1:1702/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": 123,
        "model_params": {
            "columns": [
                "building_id",
                "floor",
                "kitchen_area",
                "rooms",
                "total_area",
                "latitude",
                "longitude",
                "ceiling_height",
                "floors_total",
                "1/floor",
                "exp(rooms)",
                "1/building_id",
                "1/floors_total",
                "flats_count**3",
                "building_type_int**3",
                "has_elevator",
                "floor**3",
                "1/flats_count"
            ],
            "data": [
                [
                    14234,
                    12,
                    9,
                    2,
                    54,
                    55.90396881103516,
                    37.59132385253906,
                    2.700000047683716,
                    12,
                    0.08333333333333333,
                    7.38905609893065,
                    0.0000702543206407194,
                    0.08333333333333333,
                    86350888,
                    64,
                    1,
                    1728,
                    0.0022624434389140274
                ]
            ]
        }
    }'
```


## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию
cd services
# команда сборки контейнера
docker build -t ml_service:1.0 .
# команда для запуска микросервиса в режиме docker container
docker run --name ml_service_container --env-file .env -p 1703:1703 ml_service:1.0
```

### Пример curl-запроса к микросервису

```bash
curl -X POST "http://127.0.0.1:1703/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": 123,
        "model_params": {
            "columns": [
                "building_id",
                "floor",
                "kitchen_area",
                "rooms",
                "total_area",
                "latitude",
                "longitude",
                "ceiling_height",
                "floors_total",
                "1/floor",
                "exp(rooms)",
                "1/building_id",
                "1/floors_total",
                "flats_count**3",
                "building_type_int**3",
                "has_elevator",
                "floor**3",
                "1/flats_count"
            ],
            "data": [
                [
                    14234,
                    12,
                    9,
                    2,
                    54,
                    55.90396881103516,
                    37.59132385253906,
                    2.700000047683716,
                    12,
                    0.08333333333333333,
                    7.38905609893065,
                    0.0000702543206407194,
                    0.08333333333333333,
                    86350888,
                    64,
                    1,
                    1728,
                    0.0022624434389140274
                ]
            ]
        }
    }'
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию
cd services
# команда для запуска микросервиса в режиме docker compose
docker compose build
docker compose up
```

### Пример curl-запроса к микросервису

```bash
curl -X POST "http://127.0.0.1:1703/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": 123,
        "model_params": {
            "columns": [
                "building_id",
                "floor",
                "kitchen_area",
                "rooms",
                "total_area",
                "latitude",
                "longitude",
                "ceiling_height",
                "floors_total",
                "1/floor",
                "exp(rooms)",
                "1/building_id",
                "1/floors_total",
                "flats_count**3",
                "building_type_int**3",
                "has_elevator",
                "floor**3",
                "1/flats_count"
            ],
            "data": [
                [
                    14234,
                    12,
                    9,
                    2,
                    54,
                    55.90396881103516,
                    37.59132385253906,
                    2.700000047683716,
                    12,
                    0.08333333333333333,
                    7.38905609893065,
                    0.0000702543206407194,
                    0.08333333333333333,
                    86350888,
                    64,
                    1,
                    1728,
                    0.0022624434389140274
                ]
            ]
        }
    }'
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует <...> запросов в течение <...> секунд ...

```
# команды необходимые для запуска скрипта
...
```

Адреса сервисов:
- микросервис: http://localhost:<port>
- Prometheus: ...
- Grafana: ...