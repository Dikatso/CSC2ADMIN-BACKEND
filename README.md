## Setup virtual environment

```sh
"cd into project first!"
python3 -m venv .venv
source .venv/bin/activate
```

## Install requirements

```sh
pip install -r requirements.txt
```

## Start server

```sh
uvicorn main:app --reload
```

## After installing packes

> run
```sh
pip freeze > requirements.txt
```

> generate prisma client
```sh
prisma generate
```