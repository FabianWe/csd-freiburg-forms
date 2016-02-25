FROM django:1.9.1-python3

MAINTAINER Fabian Wenzelmann <fabianwenzelmann@posteo.de>

ENV PYTHONUNBUFFERED 1

# install all required packages
RUN apt-get update && apt-get install -y python3-dev

RUN pip install --upgrade pip

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD ./csd_freiburg_forms /code/

WORKDIR /code
