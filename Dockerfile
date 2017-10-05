FROM python:3
RUN apt-get update
RUN apt-get install -y python3-gdal
ENV PYTHONUNBUFFERED 1
RUN mkdir /project
WORKDIR /project
ADD ./requirements.txt /project/
RUN pip3 install -r requirements.txt
ADD . /project/
ENTRYPOINT ["/project/docker/entrypoint.sh"]
