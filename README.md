# Pymusic

Website for listenting to music

## Installation



```bash
pip install requirements.txt
```

```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```

```bash
redis-server
```
```bash
celery -A pymusic worker --loglevel=info
```
```bash
python manage.py runserver
```
