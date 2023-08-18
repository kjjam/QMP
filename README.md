
# Django Cache-Managemnet API

QMP is a django Cache-Managemnet API that people can sign-up and manage their cache flow.

QMP is headless and you can use your own front-end .




## Requirements

- Python 3.9
- Django 4.2
- DRF (django-rest-framework) 3.14
- Postgresql
## Features

- Headless
- token-based autentication
- Rich filtering mechanism



## Installation

### Local Installation
- 1- clone the repository:
`git clone https://github.com/kjjam/QMP.git`

- 2- install requirements:
`pip install -r ./requirements.txt`

- 3- create tables:
`python manage.py migrate`

- 4- usage (`localhost:8000/`):
`python manage.py runserver`

### Docker Installation
- 1- clone the repository
`git clone https://github.com/kjjam/QMP.git`

- 2- build and up docker-compose
`docker-compose -f docker-compose.yml up --build -d`
- 3- make applications tables:
`docker-compose -f docker-compose.yml exec web python manage.py migrate`
- 4- collect static files:
`docker-compose -f docker-compose.yml exec web python manage.py collectstatic`
- 5- access the api :
`localhost:1337/`
## End-Points

### accounts/login:
- url = `"accounts/login"`
- method = POST
- content-type =`"application/json"`
- request:
`json = {"username":<str>, "password":<str>}`
- response body:
`response= {"token":<str>}`
- response not athenticated(status=400):
response=`{"non_field_errors":["Unable to log in with provided credentials."]}`

### accounts/signup:
- url = `"accounts/signup"`
- method = POST
- content-type =`"application/json"`
- request:
`json = {"username":<str>, "password":<str>}`
- response body:
`response= {"username":<str>}`

### accounts/logout:
- url = `"accounts/logout"`
- method = GET
- content-type =`"application/json"`
- Authorization header = `"Authorization: Token <token>"`
- response body (status=200):
`response= {"username":<str>}`
- response uauthorized(status=401):
`{"detail": "Authentication credentials were not provided."}`


### /insert-transaction:
- url = `"/insert-transaction"`
- method = POST
- content-type =`"application/json"`
- Authorization header = `"Authorization: Token <token>"`

- request body:
```json
{
    "amount":100, 
    "type":"I",
    "category":1,
    "date":"2023-01-01T00:00:00"
    }
```
- response body (status=200):
```json
{
    "id": 1,
    "amount":100, 
    "type":"I",
    "category":1,
    "date":"2023-01-01T00:00:00"
    }
```
- response uauthorized(status=401)
- respose bad-request(status=400)



### /update-transaction:
- url = `"/update-transaction/<int:pk>"`
- method = PATCH
- content-type =`"application/json"`
- Authorization header = `"Authorization: Token <token>"`

- request body:
```json
{
    "amount":100, 
    "type":"I",
    "category":1,
    "date":"2023-01-01T00:00:00"
    }
```
- response body (status=200):
```json
{
    "id": 1,
    "amount":100, 
    "type":"I",
    "category":1,
    "date":"2023-01-01T00:00:00"
    }
```
- response uauthorized(status=401)

### /delete-transaction:
- url = `"/delete-transaction/<int:pk>"`
- method = DELETE
- content-type =`"application/json"`
- Authorization header = `"Authorization: Token <token>"`

- response body (status=204):
- not found or not accessed transaction(status=404)
- response uauthorized(status=401)


### /transaction/pk:
- url = `"/transaction/<int:pk>"`
- method = GET
- content-type =`"application/json"`
- Authorization header = `"Authorization: Token <token>"`

- response body (status=200):
```json
{
    "id":1,
    "amount":100, 
    "type":"I",
    "category":1,
    "date":"2023-01-01T00:00:00"
    }
```
- not found or not accessed transaction(status=404)
- response uauthorized(status=401)


### /transaction:
- url = `"/transaction?{query-params}`
- method = GET
- filtering_lookups (use any one you wany)=
  - example : /transaction?date__gt=2019-10-10T12:50:20
  - use below query params:

[

    type = type is exactly E or I
    category = category is exact the id of category
    amount__lt = amount is less than
    amount__gt = amount is greater than
    date__lt = date is less than
    date__gt = date is greater than
]
- content-type =`"application/json"`
- Authorization header = `"Authorization: Token <token>"`

- response body (status=200):
```json
[
    {
        "id":1,
        "amount":100, 
        "type":"I",
        "category":1,
        "date":"2023-01-01T00:00:00"
    },
    {
        "id":2,
        "amount":100, 
        "type":"I",
        "category":1,
        "date":"2023-01-01T00:00:00"
    }
 ]
```
- response uauthorized(status=401)

### /report:
- url = `"/report{query-params}"`
- method = GET
- date_lookups=
  - example : /report?date__gt=2019-10-10T12:50:20
  - use below query params:

[

    date__lt = date is less than
    date__gt = date is greater than
]
- content-type =`"application/json"`
- Authorization header = `"Authorization: Token <token>"`

- response body (status=200):
```json
 [

    {
        "month": "2023-01-01T00:00:00",
        "expenses": 200,
        "incomes": 500
    },
    {
        "month":"2023-02-01T00:00:00",
        "expenses": 550,
        "incomes": 100
    }
]

```
- response unauthorized(status=401)



## Middlewares
There is a middleware implemented in the project to block non-json requests.

This behaviour can be changes in setting.py :

`ALLOWED_JSON_URLS = ["admin"]`

By the above line , the application accepts `/admin/*` request in non-json content type.
##  Contributing

- Git clone https://github.com/kjjam/QMP.git
- Make the changes.
- Write your tests.
- If everything is OK. push your changes and make a pull request.

