import aiofiles
from aiohttp import web

routes = web.RouteTableDef()

gatheredFiles = []


async def generateFiles():
    for file in gatheredFiles:
        async with aiofiles.open(f"korika/{file['filename']}", mode="a") as f:
            print(f"Generating {file['filename']}...")
            await f.write(file["content"])


@routes.post("/gatherData")
async def gather_data(request):
    req = await request.json()
    print(req)

    gatheredFiles.extend(req)
    print(len(gatheredFiles))

    if len(gatheredFiles) > 1:
        await generateFiles()

    return web.json_response(
        {
            "status": "ok",
        },
        status=200,
    )


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8004)
