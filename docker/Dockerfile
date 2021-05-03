FROM python:3.7-slim
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y curl
RUN apt-get update && apt-get install -y git
RUN apt-get install -y vim less
RUN pip install --upgrade pip

ADD requirements.txt /work_dir/
WORKDIR /work_dir
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/srymh/MkdocsTagPlugin.git#egg=mdoctag