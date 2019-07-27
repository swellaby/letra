from aiohttp import ClientSession
from .http_response import HttpJsonResponse


async def request_json(
    url: str, http_verb: str = "get", headers: dict = {}, **kwargs
):
    headers["User-Agent"] = "letra"
    async with ClientSession(headers=headers) as session:
        async with session.request(
            method=http_verb, url=url, **kwargs
        ) as response:
            status = response.status
            resp_headers = response.headers
            data = await response.json()
            return HttpJsonResponse(
                status=status, headers=resp_headers, data=data
            )
