FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app/

ADD requirements.txt .

ADD wait-for-it.sh .

RUN pip install -r requirements.txt


COPY ./app /app/app