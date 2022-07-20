# Mongo DRF Endpoint Logger [MDRFEL]

![](https://forthebadge.com/images/badges/made-with-python.svg)    ![](http://forthebadge.com/images/badges/built-with-love.svg)

![](    https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![https://pypi.org/project/mongo-drf-endpoint-logger/](https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white)
![https://github.com/inanpy/mongo_drf_endpoint_logger](https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=GitHub%20Pages&logoColor=white)


![version](https://img.shields.io/badge/version-0.0.5-green.svg)
[![Open Source](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://opensource.org/)
[![Downloads](https://static.pepy.tech/personalized-badge/mongo-drf-endpoint-logger?period=total&units=none&left_color=black&right_color=orange&left_text=Total%20Downloads)](http://pepy.tech/project/mongo-drf-endpoint-logger)
[![Downloads](https://static.pepy.tech/personalized-badge/mongo-drf-endpoint-logger?period=month&units=none&left_color=black&right_color=orange&left_text=Downloads/Month)](https://pepy.tech/project/mongo-drf-endpoint-logger)
[![Downloads](https://static.pepy.tech/personalized-badge/mongo-drf-endpoint-logger?period=week&units=none&left_color=black&right_color=orange&left_text=Downloads/Week)](https://pepy.tech/project/mongo-drf-endpoint-logger)

- For your Django Rest Framework project, an API logger with MongoDb.

- It won't slow down your API's response time, because the logger runs on a different thread.

- Yes, we know that the log is not kept in the database, but there are times when we need to keep very critical data in
  the database.

- We encrypt data such as password, token, access, refresh etc. (Please read the documentation if you want to add the
  keys to be encrypted.)

- We do not log incoming urls for the admin panel.

## What data does it record?

```text
Url
Body 
Method
Ip
Response
Status Code
Execution Time
Created Date
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install mongo_drf_endpoint_logger.

```bash
pip install mongo_drf_endpoint_logger
```

## Configuration

1. Include `EndpointLoggerMiddleware` to MIDDLEWARE

```python
MIDDLEWARE = [
    # ....................................
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mongo_drf_endpoint_logger.middleware.endpoint_logger_middleware.EndpointLoggerMiddleware'
]
```

2. Add MongoDb config to `settings.py`

```
import mongoengine
mongoengine.connect(
    db="logging", # MongoDb DB name
    host="localhost", # MongoDb Host
    username="***", # MongoDb Username
    password="***", # MongoDb Password
)
```

## Config for MDRFEL

#### 1. Open the MDRFEL system:

```python
# Default: False, Description: Open The MDRFEL system:)
MONGO_DRF_ENDPOINT_LOGGER_LOG_TO_DB = True
```

#### 2. Path type

```python
# Default: "ABSLOLUTE", Description: Url path type information.
# ABSOLUTE_URI, FULL_PATH_URI, RAW_URI
MONGO_DRF_ENDPOINT_LOGGER_PATH_TYPE = "ABSOLUTE_URI"
```

#### 3. Skip URL to logging.

```python
# Default: [], Description: By using the API's url name, you can avoid logging any API.
# Example: router.register(r'detail', DetailView, basename='ApiDetail')
# You could use basename-request_type
MONGO_DRF_ENDPOINT_LOGGER_SKIP_URL_NAME = ['ApiDetail-list', 'ApiDetail-create']
```

#### 4. Skip namespace to logging.

```python
# Default: []
# Description: By specifying the app's namespace as list
# you can avoid logging the entire app into the database.
MONGO_DRF_ENDPOINT_LOGGER_SKIP_NAMESPACE = ['name_space_1', 'name_space_2']
```

#### 5. Specific methods to logging.

```
# Default: [] # Log all request.
# Description: By specifying request methods you can log only specific methods.
MONGO_DRF_ENDPOINT_LOGGER_METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'] 
```

#### 6. Specific Status Code to logging.

```
# Default: [] # Log all request.
# Description: By specifying status codes you can log only specific status codes.
MONGO_DRF_ENDPOINT_LOGGER_STATUS_CODES = ['500', '400', '422']
```

#### 7. Hide private information from logging.

```
# Default: ['password', 'token', 'access', 'refresh']
# Description: You could hide sensitive information from being exposed in the logs.
MONGO_DRF_ENDPOINT_LOGGER_STATUS_CODES = ['email', 'password']
```

## Manual Log Insert

```python
from mongo_drf_endpoint_logger.helpers import insert_log

data = {
    'url': 'testURL',
    'headers': {
        'hkey': 'hvalue',
        'token': '12345'
    },
    'body': {
        'bkey': 'bvalue'
    },
    'ip': '127.0.0.1',
    'response': {
        'rkey': 'rvlue'
    },
    'status_code': '200',
    'execution_time': '123',
    'created_date': "2022-07-11 15:19:41.184786",
    'method': 'POST'
}

insert_log(data)
# It's would work with different thread.
```

## TODO

1. Django Admin Integration
2. Interval Information for Readme
3. Unit Tests 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
