"""FastAPI-приложение для получения предсказаний модели."""

from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from fast_api_handler import FastApiHandler


class ModelParams(BaseModel):
    """Параметры модели в формате pandas orient='split'."""

    columns: list[str] = Field(
        ...,
        description="Список названий признаков модели.",
    )
    data: list[list[Union[int, float]]] = Field(
        ...,
        description="Список объектов для предсказания. Каждая строка соответствует одному объекту.",
    )


class PredictionRequest(BaseModel):
    """Формат входного запроса к микросервису."""

    user_id: Union[int, str] = Field(
        ...,
        description="Идентификатор пользователя или запроса.",
        example=123,
    )
    model_params: ModelParams = Field(
        ...,
        description="Признаки объектов, для которых нужно получить предсказание.",
    )

    class Config:
        schema_extra = {
            "example": {
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
                        "1/flats_count",
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
                            0.0022624434389140274,
                        ]
                    ],
                },
            }
        }


app = FastAPI(
    title="Real Estate Prediction Service",
    description="FastAPI-микросервис для получения предсказаний модели.",
    version="1.0.0",
)

app.handler = FastApiHandler()


@app.get("/")
def root() -> dict:
    """Проверка работоспособности сервиса."""

    return {"service": "prediction_service", "status": "ok"}


@app.get("/health")
def health() -> dict:
    """Health-check endpoint."""

    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictionRequest) -> dict:
    """Получает предсказание модели."""

    try:
        response = app.handler.handle(request.dict())
        return response

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении предсказания: {error}",
        )