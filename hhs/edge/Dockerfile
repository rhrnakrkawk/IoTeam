FROM python:3.10

WORKDIR /app

RUN python -m venv edge
RUN . edge/bin/activate
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt