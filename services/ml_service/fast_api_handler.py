"""Класс-обработчик для FastAPI-микросервиса."""

import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor


class FastApiHandler:
    """Класс для загрузки CatBoost-модели, валидации входных данных и получения предсказаний."""

    def __init__(self, model_path: str | None = None):
        default_model_path = Path(__file__).resolve().parents[1] / "models" / "model.cb"
        self.model_path = model_path or os.getenv("MODEL_PATH", str(default_model_path))
        self.model = self.load_model(self.model_path)

    def load_model(self, model_path: str) -> CatBoostRegressor:
        """Загружает обученную CatBoostRegressor-модель."""

        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(f"Файл модели не найден: {model_path}")

        try:
            model = CatBoostRegressor()
            model.load_model(str(model_path))
            print(f"CatBoost model loaded from {model_path}")
            return model

        except Exception as error:
            raise RuntimeError(f"Не удалось загрузить CatBoost-модель: {error}")

    def validate_params(self, params: dict) -> None:
        """Проверяет корректность входного запроса."""

        if not isinstance(params, dict):
            raise ValueError("Тело запроса должно быть JSON-объектом.")

        if "user_id" not in params:
            raise ValueError("В запросе отсутствует обязательное поле 'user_id'.")

        if "model_params" not in params:
            raise ValueError("В запросе отсутствует обязательное поле 'model_params'.")

        model_params = params["model_params"]

        if not isinstance(model_params, dict):
            raise ValueError("Поле 'model_params' должно быть JSON-объектом.")

        if "columns" not in model_params:
            raise ValueError("В 'model_params' отсутствует поле 'columns'.")

        if "data" not in model_params:
            raise ValueError("В 'model_params' отсутствует поле 'data'.")

        columns = model_params["columns"]
        data = model_params["data"]

        if not isinstance(columns, list) or len(columns) == 0:
            raise ValueError("Поле 'columns' должно быть непустым списком.")

        if not all(isinstance(col, str) for col in columns):
            raise ValueError("Все значения в 'columns' должны быть строками.")

        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Поле 'data' должно быть непустым списком.")

        for row_id, row in enumerate(data):
            if not isinstance(row, list):
                raise ValueError(f"Строка data[{row_id}] должна быть списком.")

            if len(row) != len(columns):
                raise ValueError(
                    f"Количество значений в data[{row_id}] не совпадает с количеством columns: "
                    f"{len(row)} != {len(columns)}"
                )

            for value_id, value in enumerate(row):
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(
                        f"Значение data[{row_id}][{value_id}] должно быть числом."
                    )

                if not np.isfinite(value):
                    raise ValueError(
                        f"Значение data[{row_id}][{value_id}] должно быть конечным числом."
                    )

    def predict(self, model_params: dict) -> float | list[float]:
        """Возвращает предсказания модели."""

        columns = model_params["columns"]
        data = model_params["data"]

        features = pd.DataFrame(data=data, columns=columns)

        predictions = self.model.predict(features)
        predictions = np.asarray(predictions).ravel()
        predictions = [float(pred) for pred in predictions]

        if len(predictions) == 1:
            return predictions[0]

        return predictions

    def handle(self, params: dict) -> dict:
        """Обрабатывает запрос к микросервису."""

        self.validate_params(params)

        user_id = params["user_id"]
        model_params = params["model_params"]

        prediction = self.predict(model_params)

        return {
            "user_id": user_id,
            "prediction": prediction,
        }