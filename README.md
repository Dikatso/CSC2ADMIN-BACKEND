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

> Generate prisma client
```sh
prisma generate
```

## Making changes to database schema
> Update the postgreSQL database after modifying the schema
```sh
prisma db push
```

> Generate new code from updated postgreSQL database
```sh
prisma generate
```

> To get newly updated database schema
```sh
prisma db pull
```

