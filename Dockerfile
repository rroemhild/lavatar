FROM google/python

ENV APP_HOST 0.0.0.0
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get -qq update \
    && apt-get install -y libjpeg-dev

WORKDIR /app

RUN virtualenv /env
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install -r requirements.txt
RUN /env/bin/pip install gevent

ADD . /app

RUN ln -sf /app/lavatar/static /static
