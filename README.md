# Online_store REST API

Для создания REST API использовались:
 - [Python](https://www.python.org/)
 - [Django](https://www.djangoproject.com/) 
 - [Django REST framework](https://www.django-rest-framework.org/)
 - Объектно-реляционная СУБД [PostgreSQL](https://www.postgresql.org/)
 - Web-сервер [Gunicorn](https://gunicorn.org/) - WSGI сервер для UNIX

Требуемые библиотеки находятся в файле requirements.txt

## Команды для запуска приложения на сервере linux
### Настройка PostgreSQL
    1. sudo apt-get install postgresql
    2. sudo apt-get install postgresql-server-dev-all
    3. sudo -u postgres psql postgres
        a. \password postgres
        b. Ввод пароля: secret
        c. Создал пользователя online_store
            create user online_store with password 'secret';
            alter role online_store set client_encoding to 'utf8';
            alter role online_store set default_transaction_isolation to 'read committed';
            alter role online_store set timezone to 'UTC';
        d. create database online_store_db owner online_store;
        e. Выйти из postgres (\q)   
### Клонирование репозитория
    1. sudo apt install git
    2. mkdir project && cd project
    3. git clone https://github.com/Borutia/online_store.git
    Проект теперь находится в ~/project/online_store
    4. cd online_store/
### Установка python и venv
    1. sudo apt-get install python3
    2. sudo apt-get install python3-venv
    3. python3 -m venv venv
    4. Из папки проекта: source ./venv/bin/activate
    5. pip install -r requirements.txt
### Настройка проекта 
    1. python manage.py makemigrations
    2. python manage.py migrate
### Развёртывание сайта
    1. pip install gunicorn   
    2. gunicorn -b :8080 online_store.wsgi 
### Запуск тестов
    1. sudo -u postgres psql postgres
    2. ALTER USER online_store CREATEDB;
    3. Самописные тесты запускаются командой: python manage.py test
    4. Ручное тестировать можно проводить с помощью Postman
