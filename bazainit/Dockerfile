FROM python:3.10

RUN pip install aiosqlite asyncio aiohttp aiofiles

COPY BazaInit.py ./

COPY korika.db ./



CMD [ "python", "./BazaInit.py" ]
