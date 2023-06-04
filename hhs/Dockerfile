FROM python:3.10

WORKDIR /app

RUN python -m venv restaurant
RUN . restaurant/bin/activate
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt