FROM python:3.7-slim-stretch

ENV APP_HOST 0.0.0.0

# Install packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -qq update \
    && apt-get install -y libjpeg-dev

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gevent

ADD . /app

RUN ln -sf /app/lavatar/static /static

USER nobody

EXPOSE 5000

CMD []
ENTRYPOINT ["python", "/app/production.py"]
