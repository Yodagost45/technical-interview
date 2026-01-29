# Junior Software Engineer Challenge

This challenge is designed to assess your ability to work in a python development scenario. You will find a trivial FastAPI application in the `app/` directory. It currently has a number of simple routes and boilerplate code.

You can run the development server with the following command:

```bash
uv run alembic upgrade head # This creates the sqlite database db.sqlite, you only need to run it once.
uv run pydantic dev
```

You must perform the following tasks.

## Task 1: NMEA Parsing

NMEA is a data format used by numerous GPS recievers. It is a line-based plaintext format. As part of this challenge, a file `output.nmea` has been provided with a number of synthetic NMEA sentences.

You must create a Python executable file which parses the NMEA file and POSTs location information to the FastAPI server.

You are allowed to parse the file yourself, or use one of a number of packages on PyPI which support parsing NMEA.

Please write at least one unit test that ensures your parsing logic is correct.

## Task 2: Speed Calculation

Using the data you have ingested in task 1, create a route `GET /vehicles/{id}/speed` that calculates the mean average speed that a vehicle has travelled throughout its existence. Calculate the speed using the pairwise distance between locations divided by the time between locations.
