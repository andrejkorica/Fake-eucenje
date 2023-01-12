FROM python:3.10

RUN pip install aiohttp aiofiles

COPY gatherData.py ./

RUN mkdir korika

CMD [ "python", "./gatherData.py" ]

