FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . ./frontend
WORKDIR ./frontend


CMD ["python", "-m", "main"]
