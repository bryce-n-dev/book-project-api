# Book Project API

Book Project API is a REST API built with FastAPI, SQLAlchemy, and SQLite.

## Installation

Run the follow code below to create a virtual environment and install the required dependencies. Note that this has only been tested on version `Python 3.8.13`.

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### For Windows

```sh
python -m venv venv
cd venv/Scripts/
activate
cd ../..
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install httpx
pip install pytest
```

## Usage

To run the server, run the following command.

```sh
uvicorn main:app --reload
```

By default, the server will run on port 8000.

To run static type checking with mypy, run the following command.

```sh
mypy main.py
```

To run all unit tests, run the following command.

```sh
pytest
```
