FROM python:3.7-slim

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

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive

# mkdocsのインストール
ADD requirements.txt /work_dir/
WORKDIR /work_dir
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/srymh/MkdocsTagPlugin.git#egg=mdoctag

# drawioのインストール
ENV DRAWIO_VERSION 14.6.13

RUN apt-get install -y wget libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils libatspi2.0-0 libappindicator3-1 libsecret-1-0 libgbm-dev libasound2 xvfb
RUN wget https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb
RUN dpkg --install drawio-amd64-${DRAWIO_VERSION}.deb
RUN rm drawio-amd64-${DRAWIO_VERSION}.deb

# https://github.com/jgraph/drawio-desktop/issues/127 これでいけた
RUN apt-get install -y xvfb
RUN echo "#!/bin/sh\nxvfb-run /usr/bin/drawio \"\${@}\"" > /usr/local/bin/drawio && \
    chmod +x /usr/local/bin/drawio

EXPOSE 8888