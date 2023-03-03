# database_api
Uses FastAPI to perform CRUD operations in an Oracle database


## Setup
Rename `config.py.template` to `config.py` and set database connection parameters within it.

## Launching

```
pipenv shell
uvicorn main:app --reload
```