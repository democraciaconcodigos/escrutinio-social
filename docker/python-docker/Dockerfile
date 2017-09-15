FROM python:3
RUN apt-get update
RUN apt-get install -y python3-gdal
ENV PYTHONUNBUFFERED 1
RUN mkdir /project
WORKDIR /project
ADD local-settings-docker.py /tmp/
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
