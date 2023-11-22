# DTrade

## Features✨

### Market:

- real-time price
- search any cryptocurrency!

### Trade:

- spot trading
- limit-order trading
- recent trades(Live)
- all trade histories
- all open orders
- cancel open orders

### Portfolio:

- account available margin
- account total margin
- PNL chart
- asset allocation chart

### Trade history

- all trade histories

### Open orders:

- all open orders
- cancel orders

### Profile:

- gravatar profile photo
- edit name and last name
- change password
- view email and username

## Tech

All used frameworks, technologies and libraries:

- [Django] - Backend
- [Redis] - Datebase memory caching
- [PostgreSql] - Datebase
- [JavaScript] - Frontend
- [Twitter Bootstrap] - UI boilerplate
- [Sentry] - Error tracking
- [Google analytics] - Analysis
- [Celery] - Task scheduling
- [Docker] - Containerization
- [Django channels] - Web-sockets

## Docker

`$ docker-compose up --build`

## Setting Up Super User

- To create a **superuser account**, use this command:

  $ python manage.py createsuperuser

## Local setup

`$ cd web`</br>
`$ cp .env-sample .env` and paste variables with your own.</br>
`$ pip install -r requirements/local.txt`</br>
`$ chmod +x ./release.sh && ./release.sh`</br>
`$ python manage.py collectstatic`</br>
`$ python -m celery -A config worker -l info -c 4`</br>
in another console run:</br>
`$ python manage.py runserver`</br>
