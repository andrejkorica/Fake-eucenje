import aiohttp
from aiohttp import web

routes = web.RouteTableDef()


async def extrudeDictionary(data):
    filtered_data = []
    for item in data:
        if item['username'].startswith('w'):
            filtered_data.append(item)
    print(len(filtered_data))
    return filtered_data


@routes.post("/wt")
async def wt(request):
    try:
        req = await request.json()
        data = await extrudeDictionary(req["data"])
        print(len(data))

        async with aiohttp.ClientSession() as s:
            r = await s.post(
                "http://gatherdata:8004/gatherData", json=data
            )
            print(r)
        return web.json_response(
            {"service_id": 3, "response": r},
            status=200,
        )
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8002)
