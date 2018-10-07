FROM python:2

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./python/main/main.py", "--interval", "60", "--top", "200" ]
