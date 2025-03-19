# test
test task for internship opportunity in KODE


Table of contents:
- [Running instructions](#running-instructions)
- [Environment variables](#environment-variables)
- [Documentation](#documentation)
  - [Project settings](#settings)
  - [Schedule model](#schedule-sqlalchemy-table-model)
  - [Endpoint docs](#endpoint-docs)

## Running instructions
1. Set up a PostgreSQL database
2. create .env file in the root directory of the project and fill 
it with [required environment variables](#environment-variables) in format

> VARNAME1=value1
> 
> VARNAME2=value2
3. install dependencies
from root directory run in your system's CLI:
```bash
pip install requirements.txt 
```
4. Run service
For that switch to "/src" directory and launch fastapi; in Linux sh it may be done with
```sh
cd src
fastapi dev main.py
```

## Environment variables

Environment variables to be specified in .env file (in the root directory of the project) required to 
bring service to life:

| variable | value |
| -------- | ----- |
| POSTGRES_USER | username of PostgreSQL user |
| POSTGRES_PASSWORD | password for given user |
| POSTGRES_DB | name of the database |


## Documentation

### settings
settings.py module stores service configuration; contained variables are:

| variable | value |
| -------- | ----- |
| POSTGRES_USER | represents POSTGRES_USER env variable |
| POSTGRES_PASSWORD | represents POSTGRES_PASSWORD env variable |
| POSTGRES_DB | represents POSTGRES_DB env variable |
| CLOSE_PERIOD | datetime.timedelta object configuring for what time period should "/next_takings" endpoint calculate takings |
|||
| HOUR_START | specifies start of the day hour, defaults to 8 |
| HOUR_END | specifies end of the day hour, defaults to 22 |

### Schedule SQLAlchemy table model

- hf

### Endpoint docs
#### /schedule
INPUT DATA FORMAT

Required input JSON keys:
- name - representing name of the medicine
- period - representing period of time with which medicine must be taken; 
must be specified whether as an **integer** (then considered time in seconds) or 
in [ISO8601 format](https://en.wikipedia.org/wiki/ISO_8601)
- user_id - id of an animal to use it 

Optional input JSON keys:
- duration - treatment duration; if not provided treatment course is considered eternal. 
Should be whether a valid int value (thus interpreted as amount of seconds) or in 
[ISO8601 format](https://en.wikipedia.org/wiki/ISO_8601)
- start_date - time for starting the treatment course, if not provided considered to be 
the time of schedule creation. Should be either valid int value (thus interpreted as amount 
of seconds since [UNIX epoch](https://en.wikipedia.org/wiki/Unix_time)) or in 
one of following formats:
  - YYYY-MM-DDTHH:MM:SS.f
  - YYYY-MM-DD 
