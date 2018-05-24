FROM python:3.6-slim

RUN set -e && \
  apt-get update && \
  apt-get install -y git && \
  pip install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip install -r /app/requirements.txt

ENV DOCKER=1

CMD ["/app/run-demo.sh"]




