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

## Running tests
> Make sure venv environment is active and server is running, and execute the command
```sh
pytest -v
```
> Note: the file.txt file gets deleted after running the test, so make sure to create another one before running the test again
