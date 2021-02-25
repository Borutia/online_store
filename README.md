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
        b. Пароль: secret
        c. Создал пользователя online_store
            ```sql
            create user online_store with password 'secret';
            alter role online_store set client_encoding to 'utf8';
            alter role online_store set default_transaction_isolation to 'read committed';
            alter role online_store set timezone to 'UTC';
        d. create database online_store_db owner online_store;
        e. Выйти из postgres (\q)   
### Клонирование репозитория
    1. sudo apt install git
    2. cd ~/project 
    3. git clone git@github.com:Borutia/online_store.git
    Проект теперь находится в ~/project/online_store
### Установка virtualenv
    1. sudo apt-get install python3-venv
    2. python3 -m venv venv
    3. Из папки проекта  source ./venv/bin/activate
    4. pip3 install -r requirements.txt
### Настройка проекта 
    1. ./manage.py makemigrations
    2. ./manage.py migrate
### Развёртывание сайта
    1. pip install gunicorn   
    2. Сайт перезапускает Supervizor, если возникнут неполндки, то запуск осуществляется 
    из папки проекта gunicorn -b :8080 OnlineStoreREST.wsgi 
### Настройка тестов
    1. sudo -u postgres psql postgres
    2. ALTER USER online_store CREATEDB;
    3. Далее тесты вызаваются командой: ./manage.py test
