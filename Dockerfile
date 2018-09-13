FROM python:3.6

RUN set -e && \
  apt-get update && \
  apt-get install -y git curl && \
  pip install --upgrade pip && \
  apt-get clean

COPY . /app

WORKDIR /app

# We force nbconvert<5.4 due to incompatible versions of mistune
RUN pip install -e git+https://github.com/SwissDataScienceCenter/renku-python.git#egg=renku && \
    pip install "nbconvert<5.4" && \
    pip install -e ./demo-script/commits/03/src/python/weather-ch

ENV DOCKER=1

CMD ["/app/run-demo.sh"]
