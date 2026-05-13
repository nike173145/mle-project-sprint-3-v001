FROM python:3.11-slim

LABEL author=${AUTHOR}
# ${AUTHOR} - это переменная среды

COPY . ./ml_service
WORKDIR ml_service 
RUN pip3 install -r requirements.txt
VOLUME /models

EXPOSE ${APP_PORT}
# указываем переменную среды

CMD uvicorn ml_service.main:app --host  0.0.0.0 --port ${APP_PORT}
# изменили команду на простую строку