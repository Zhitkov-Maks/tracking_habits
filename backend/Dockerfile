FROM python:3.12.0-alpine3.18

RUN apk update && apk add --no-cache curl && rm -rf /var/cache/apk/*

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . ./backend
WORKDIR ./backend

CMD ["sh", "-c", "python migrate.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
