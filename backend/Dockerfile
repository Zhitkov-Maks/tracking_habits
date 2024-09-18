FROM python:3.12.0-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . ./backend
WORKDIR ./backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
