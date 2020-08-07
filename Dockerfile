FROM python:3.7.5-slim-buster
MAINTAINER Ajay Patil <ajay.patil.ap01@gmail.com>

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /manager
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY req.txt req.txt
RUN pip install -r req.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -c "python:config.gunicorn" "manager.app:create_app()"
