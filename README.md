# test
test task for internship opportunity in KODE


Table of contents:
- [Running instructions](#running-instructions)
- [Environment variables](#environment-variables)
- [Documentation](#documentation)
  - [Project settings](#settings)
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
| POSTGRES_USER ||
| POSTGRES_PASSWORD ||
| POSTGRES_DB ||
| CLOSE_PERIOD ||

### Endpoint docs
#### /schedule
INPUT DATA FORMAT

Input data must contain following fields:
- name - representing name of the medicine
- period - representing period of time with which medicine must be taken; 
must be specified whether as an **integer** (then considered time in seconds) or 
in [ISO8601 format](https://en.wikipedia.org/wiki/ISO_8601)
- end_date (OPTIONAL) - date of stopping taking medicine; if not provided 
medicine is considered to be eternal. Should be whether a valid int value (thus interpreted 
as amount of seconds since 1.1.1970) or in one of given formats:
  - YYYY-MM-DDTHH:MM:SS.f 
  - YYYY-MM-DD
- user_id - id of an animal to use it 

