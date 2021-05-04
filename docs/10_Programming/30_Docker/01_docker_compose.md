---
title: DockerComposeを使ってVolumeを指定してコンテナを起動する
tags:
    - Docker
    - 環境構築
    - VSCode
description: DockerComposeからコンテナ起動してVolume指定するあたり
---

[Dockerimageをつくる](00_dockerfile.md)で、コンテナを作るための土台となる
イメージをつくることができました。
しかし、前回のようにコンテナ内に直接コードを置いたり
出力ファイルを書いたりすると、コンテナを削除して作り直したりするたびに
データが消えてしまいます。

Dockerは、 コンテナを起動・削除を繰り返し、シンプルで再現可能な環境を
利用するのが一般的です。

なので、コンテナ内でなにかしたい（コンテナ内でコマンドを実行したり、テストしたり）
したい場合は、Volumeを作成して、それをコンテナ内にマウントするようにします。

これは、PCの環境にNASの共有ドライブを接続したり、ドライブレターにマウントする
のと同じような感じです。

このあたりの処理をする場合、コマンドでやってもよいのですが
非常にめんどくさいので Docker Compose という機能を利用して
指定のイメージを起動できるようにします。

## docker-compose.yml を準備する

![](https://gyazo.com/0f4c0a6d94de74022aee959580c32caa.png)

まず、フォルダ構成。

Dockerのイメージを構築するのに必要なファイル（Dockerfile）と
コンテナ起動の設定ファイルとも言える docker-compose.yml をまとめたフォルダと
Dockerのコンテナでマウントするための src フォルダを用意します。

```yml
version: "3"

services:
  pythontest:
    build:
      context: .
      dockerfile: ./Dockerfile
    container_name: pythontest
    stdin_open: true
    volumes:
      - ../src:/work_dir
    working_dir: /work_dir
```

docker-compose.yml はこんなかんじ。

version: "3" は、この compose の書式のバージョンのことで、お約束として書いておきます。

次に、起動したいコンテナの情報を services 以下に書きます。
今回は１つだけですが、この下に複数のコンテナを書いておいて
それを連携させるようなことも可能です。

起動したいコンテナは、 Dockerfile をベースにしてビルドする必要があります。
事前にビルド結果をDockerHubにあげておくとかもできますが
上の例のように、 build: 以下に dockerfile を指定することで、
Dockerfileからイメージをビルドして、そのイメージからコンテナを起動する...というように
一連の処理を自動化することができます。

そして volumes の指定。
書き方は ローカル環境のディレクトリ:マウント先
のように書きます。
なので、ここでは src ディレクトリを、コンテナ内から参照するという意味になります。

working_dir は、コンテナを起動したときのデフォルトディレクトリです。
今回はマウントしたディレクトリがワークディレクトリになるようにしました。

stdin_open: true は、コマンドラインからコンテナを起動した場合、
エラーになってしまうのの対策です。

準備ができたら、VSCodeから起動します。

![](https://gyazo.com/13df3b72eb41d0b7135af6327730cfa8.png)

Docker Compose Up を実行すると、

![](https://gyazo.com/054070476d8e34ccffa06523137d09d3.png)

イメージのビルドが走り、コンテナを起動することができます。

起動できたら、Dockerの CONTAINERSからAttach Visual Studio Code
をクリックして、コンテナのにアタッチします。
アタッチしたら、フォルダーをワークスペースに追加を選び、

![](https://gyazo.com/ad524548521c35a8c4cc413eddb58e66.png)

/work_dir を選択します。

![](https://gyazo.com/85367ed2bdde44fe187f2864663ea085.png)

コンテナにアタッチした状態でも、Volumeで指定したローカルPCの
ディレクトリがマウントできているのがわかります。

これで、コンテナを削除→起動し直した場合も
コンテナはリセットされますが、各種データは残った状態になります。