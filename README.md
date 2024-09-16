# TRACKING HABITS BOT VERSION 0.1.1

Телеграмм бот для отслеживания привычек.


## Запуск проекта

### Зависимости необходимые для запуска и подготовки проекта
- У вас должен быть установлен докер.
- Должен быть установлен openssl для генерации ключей для JWT
- У вас есть токен для телеграм бота подробнее - [Статья на Хабр](https://habr.com/ru/post/262247/)

### Подготовка проекта

- Зайдите в директорию backend и создайте директорию certs
- Перейдите в certs и выполните команды.


```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

- Так же вам нужны переменные окружения, для этого создайте 
файл .env и добавьте необходимые переменные, пример в файле .env.template .

### Запуск проекта

- Проект запускается командой

```commandline
docker compose up -d
```

- Далее нужно применить миграции для создания таблиц в бд.

```commandline
alembic upgrade head
```

- Приложение готово к работе.
