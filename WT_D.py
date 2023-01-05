import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

async def extrudeDictionary(data):
    filtered_data = []
    for item in data:
        if item['username'].startswith('d'):
            filtered_data.append(item)
    return filtered_data

@routes.post("/wt")
async def wt(request):
    try:
        req = await request.json()
        data = await extrudeDictionary(req["data"])
        async with aiohttp.ClientSession() as s:
            r = await s.post(
                "http://127.0.0.1:8004/gatherData", json=data
            )
        return web.json_response(
            {"service_id": 2, "response": r},
            status=200,
        )
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8003)