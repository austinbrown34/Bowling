# bowling

An API and Data Model for managing the interactions of a game of bowling.

## Getting Started

This project has CircleCI integration with workflows that push staging and master builds to Heroku. Be sure to modify this in the .circleci/config.yml and/or include necessary environment variables in CircleCI.

Also, to run locally, make sure you have a PostGres client installed on your computer.

### Prerequisites

To avoid potential conflicts, create a virtual environment and activate it before following installation instructions.

```
virtualenv env
. env/bin/activate
```

### Installing

Follow these steps to setup bowling.

Install dependencies

```
pip install -r requirements.txt
python manage.py migrate
```

### Usage

To run locally (for POSTS) be sure to use something like ngrok and add that ngrok url to your ALLOWED_HOSTS in settings.

```
python manage.py runserver
ngrok http 8000 (or whatever port your app is running on)
```

Here are some examples of interacting with the API:

```
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"name": "test", "user": {"username": "test12345", "password": "12345"}}' http://9ade256b.ngrok.io/api/v1/player/create/\?username\=admin\&api_key\=test

localhost:8000/api/v1/gamemanager/new_game/?players=8,10&username=admin&api_key=test

localhost:8000/api/v1/game/31/start/?username=admin&api_key=test

localhost:8000/api/v1/game/31/bowl/?mark=5&username=admin&api_key=test

localhost:8000/api/v1/game/31/get_state/?username=admin&api_key=test
```

## Running the tests

```
python manage.py test
```

## Authors

* **Austin Brown**
