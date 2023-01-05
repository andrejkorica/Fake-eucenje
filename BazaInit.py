

import aiosqlite
import asyncio
from aiohttp import web
import aiofiles
import json

routes = web.RouteTableDef()

async def fillIf():
    
    async with aiosqlite.connect("korika.db") as db:
        # async with db.execute("DELETE FROM data"):
        #     await db.commit()
        if (db):
            print("BAZA SPOJENA")
            async with db.execute("SELECT COUNT(*) FROM data") as cursor:
                fetched = await cursor.fetchall()
                await db.commit()
                if fetched[0][0]:
                    print("ima", fetched[0][0], "elementa")
                else:
                    print("nema elementa")
                    await fillDB()                    
        else:
            print("Error pri spajanju")

async def fillDB():
    async with aiofiles.open("fakeDataset.json", mode="r") as fakedb:

        i = 0
        print("Punjenje baze...")
        async for cursor in fakedb:
            async with aiosqlite.connect("korika.db") as db:
                await db.execute(
                    "INSERT INTO data (username,ghlink,filename,content) VALUES (?,?,?,?)",
                    (json.loads(cursor)["repo_name"].split("/")[0], "https://github.com/" + json.loads(cursor)["repo_name"], json.loads(cursor)["path"].split("/")[-1], json.loads(cursor)["content"],),
                )
                await db.commit()
            i += 1
            if i == 10000:
                return print("Gotovo!")
                

@routes.get("/getData")
async def getData(request):
    try:
        response = {
            "data": [],
        }
        async with aiosqlite.connect("korika.db") as db:
            async with db.execute("SELECT * FROM data ORDER BY RANDOM() LIMIT 100") as cursor:
                async for row in cursor:
                    response["data"].append({'id': row[0], 'username': row[1], 'ghlink': row[2], 'filename': row[3], 'content': row[4]})
                await db.commit()
        return web.json_response(response)

    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)}, status=500)

asyncio.run(fillIf())
app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8000)