FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /target_app
WORKDIR /target_app
ADD requirements.txt /target_app/
RUN pip install -r requirements.txt
ADD . /target_app/