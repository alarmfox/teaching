FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py models.py routers.py switches.py ./

CMD ["flask", "run"]

