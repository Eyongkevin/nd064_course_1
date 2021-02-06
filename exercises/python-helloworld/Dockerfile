FROM python:alpine
LABEL maintainer="Eyong Kevin"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python","app.py"]

