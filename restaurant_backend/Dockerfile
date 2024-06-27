FROM python:3.10-slim

RUN apt-get update -y
RUN apt-get install -y pkg-config
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y gcc

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . .

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
