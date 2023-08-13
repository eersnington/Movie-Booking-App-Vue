@echo off

title "Backend | Celery"
call .\venv\Scripts\activate

cd backend

celery -A main:cel_app worker -l INFO -P gevent

PAUSE