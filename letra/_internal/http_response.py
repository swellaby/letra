from collections import namedtuple

HttpJsonResponse = namedtuple("HttpJsonResponse", "status, headers, data")
