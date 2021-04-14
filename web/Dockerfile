FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev
    
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install psycopg2

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

