FROM python:3.12-slim-bookworm
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN pip3 install -e .
ENV PYTHONUNBUFFERED=1
