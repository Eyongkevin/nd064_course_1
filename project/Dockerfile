FROM python:2.7-alpine
LABEL maintainer="Eyong Kevin Enowanyo"

COPY ./techtrends /app

WORKDIR /app

RUN pip install -r requirements.txt 

EXPOSE 3111


CMD python init_db.py ; python app.py

