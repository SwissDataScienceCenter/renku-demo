FROM python:3.6-slim

RUN set -e && \
  apt-get update && \
  apt-get install -y git curl && \
  pip install --upgrade pip && \
  apt-get clean

COPY . /app

WORKDIR /app

RUN pip install pipenv && \
    pipenv install --system && \
    pip install -e ./demo-script/commits/03/src/python/weather-ch

ENV DOCKER=1

CMD ["/app/run-demo.sh"]




