# Бэкенд для работы с платежной системой Stripe дял оплаты товаров и заказов

## Установка и запуск

1) Клонируйте git репозиторий
```commandline
git clone <адрес репозитория>
```
2) Установите виртуальное окружение:
```commandline
python -m venv venv
```
3) Создайте файл .env на основе .env_template со своими переменными
4) Установите зависимости
```commandline
pip install -r requirements.txt
```
5) Выполните миграции:
```commandline
python manage.py migrate
```
6) Запуск проекта с помощью Docker
```commandline
docker-compose up --build
```

## Работа API
Для получения HTML страницы с информацией о Item с указанным id необходимо выполнить GET-запрос по url:
```commandline
<домен>/item/{id}
```
Для получения Stripe Session Id для оплаты Item с указанным id необходимо выполнить GET-запрос по url:
```commandline
<домен>/buy/{id}
```
Для получения HTML страницы с информацией о Order с указанным id необходимо выполнить GET-запрос по url:
```commandline
<домен>/order/{id}
```
Для получения Stripe Session Id для оплаты Order с указанным id необходимо выполнить GET-запрос по url:
```commandline
<домен>/buy_order/{id}
```
