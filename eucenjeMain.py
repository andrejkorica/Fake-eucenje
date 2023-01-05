

import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/getAPI")
async def getAPI(a):
    try:
        tasks = []
        async with aiohttp.ClientSession() as session:
            req = await session.get("http://127.0.0.1:8000/getData")
            req = await req.json()
            
            tasks.append(
                asyncio.create_task(session.post("http://127.0.0.1:8002/wt", json=req))
            )
            tasks.append(
                asyncio.create_task(session.post("http://127.0.0.1:8003/wt", json=req))
            )

            await asyncio.gather(*tasks)
    


        return web.json_response({"status": "ok", "response": req}, status=200)

    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})



app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8001)




