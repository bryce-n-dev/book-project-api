# Book Project API

Book Project API is a REST API built with FastAPI, SQLAlchemy, and SQLite.

## Installation

Run the follow code below to create a virtual environment and install the required dependencies. Note that this has only been tested on version `Python 3.8.13`.

```sh
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
```

## Usage

To run the server, run the following command.

```sh
uvicorn main:app --reload
```

By default, the server will run on port 8000.