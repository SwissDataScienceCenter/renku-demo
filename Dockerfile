FROM python:3.6-slim

RUN set -e && \
  apt-get update && \
  apt-get install -y git && \
  pip install --upgrade pip

WORKDIR /app/

COPY requirements.txt ./

RUN pip install -r /app/requirements.txt

COPY users.json run-demo.sh cleanup.sh ./

COPY steps ./steps

COPY demo-script ./demo-script



