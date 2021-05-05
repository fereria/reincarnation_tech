---
title: DockerでJupyterを起動する
tags:
    - Docker
    - JupyterNotebook
---

DockerfileとDockerComposeを利用することで
コンテナを起動して、開発環境が作ることができました。

次は、DockerのコンテナでJyputerを起動して
http://localhost:8888
のように、ブラウザからDockerのコンテナ内で起動しているJupyterにアクセスしてみます。

まずはDockerfile

```
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

ADD ./usdnotebook/requirements.txt /work_dir/
ADD ./usdnotebook/jupyter_notebook_config.py /tmp/

RUN mv /tmp/jupyter_notebook_config.py ./~jupyter

WORKDIR /work_dir
RUN pip install -r requirements.txt

EXPOSE 8888
```

すでにJupyterをインストールしているイメージもありますが
Usdを利用したかったので 3.7-slimをベースにします。

```
usd-core
jupyter
jupyterlab
```
requirements.txtはこのとおり。

```
c = get_config()
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
c.NotebookApp.notebook_dir = '/work_dir'
c.NotebookApp.password = u''
```

Jupyterの設定ファイルを用意して、ADDで追加したあと
jupyter 用のフォルダ以下にコピーします。

```
version: "3"

services:
  usdnotebook:
    build:
      context: .
      dockerfile: ./usdnotebook/Dockerfile
    container_name: usdnotebook
    stdin_open: true
    volumes:
      - ../:/work_dir
    ports:
      - "8888:8888"
    environment:
      - JUPYTER_ENABLE_LAB=yes
    command: jupyter lab --NotebookApp.token='' --allow-root --no-browser --port 8888 --ip=0.0.0.0
```

最後に docker-compose.yml を書きます。

ports が、コンテナ側のポートと実際にアクセスするポートの対応関係を指定するもの
command は、コンテナ起動後に実行したいコマンドになります。

準備ができたら、 
```
docker-compose -f docker/docker-compose.yml up 
```
で、コンテナを起動します。

![](https://gyazo.com/5cdf95114d90b2aefeb2d0ca2d01b464.png)

コンテナが起動できたら、

![](https://gyazo.com/faea323e2a5dea6056ba903dabbb9764.png)

ブラウザで指定のポートにアクセスすると、Jupyter Labに接続することができます。
volumes でローカルPCのディレクトリをマウントしていれば
コンテナ内でNotebookを実行していても、データはローカルに残るので色々はかどります。