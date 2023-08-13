# App Dev 2 PROJECT

Mad 2 Project with Flask and VueJS

## Install Virtual Environment

```sh
python -m venv venv
```
## Install Node Modules

```sh
cd frontend
npm install
```

## Run Redis (WSL2)

```sh
sudo service redis-server start
redis-cli
```

## Run Celery

```sh
.\venv\Scripts\activate
cd backend
celery -A main:cel_app worker -l INFO -P gevent
```

## Run Backend 

```sh
.\venv\Scripts\activate
cd backend
python main.py
```

## Run Frontend

```sh
.\venv\Scripts\activate
cd frontend
npm run serve
```