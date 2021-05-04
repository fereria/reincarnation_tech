---
title: Dockerfileを作成してVSCodeでアタッチする
tags:
    - Docker
    - VSCode
---

DockerとGithubActionsを利用して、各種ビルドを自動化する方法まとめ。

DockerはWindows版をインストール
ビルドしたり起動したりする処理はVSCodeをメインに使用します。

## Dockerfile

まずは、Dockerfileを利用してイメージを作成します。
イメージとは、コンテナを作るための設計書のようなもので
同じ構成のコンテナを量産したり、他のPCやサーバーで同じ環境を簡単に作れます。

このイメージを作るために必要なのが Dockerfileで
このファイルに各種コマンドを記述することで、イメージを作成することができます。

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

RUN apt-get install -y curl
RUN apt-get update && apt-get install -y git
RUN apt-get install -y vim less
RUN pip install --upgrade pip

ADD requirements.txt /work_dir/
WORKDIR /work_dir
RUN pip install -r requirements.txt
```

イメージを作るときは、０からつくるというより
すでにある土台から、必要な設定などを付け足す形で作ります。

サンプルの場合は、Python3.7の基本的な構成が入ったものを使用します。

コマンドは、

FROM ベースとなるコンテナ名
RUN Linuxのコマンドを実行
ENV 環境変数を指定
ADD コンテナにファイルを追加
WORKDIR コンテナ実行時のフォルダを指定

を使用して、必要な環境設定を作成します。

コンテナは、そのままだと完全に独立した（切り離された）環境になるので、
pip install で requirements.txt を利用してインストールしたい場合
ファイルが存在しないので実行できません。
こういった、環境構築に必要なデータも、イメージ作成時に合わせてパッケージしておきます。
```
usd-core
pytest
nbconvert
```
今回の requirements.txtの中身はこんなかんじで
Usdを使えるようにしています。

## イメージビルド

Dockerfileを作成したら、イメージビルドをして、正しく構築できるか確認します。

![](https://gyazo.com/8227a3edebff0803107bb2a960002831.png)

VSCodeから Docker Images: Build Image...
を選択し、

![](https://gyazo.com/971620c8a8a930c31cf6426a8a16a468.png)

イメージ名を指定して実行します。

![](https://gyazo.com/2df7a7df48fd26630abdb355694f96ae.png)

問題なくビルドが完了すると、DockerのImagesに
Dockerfileをビルドした結果のイメージが追加されます。

![](https://gyazo.com/8de8b460a12a46315755da34263b020d.png)

タブを開いて、latest を右クリック、Runを実行すると

![](https://gyazo.com/30b25e96189cd09de1e092ac3ca821e8.png)

コンテナを起動することができました。

![](https://gyazo.com/e98c3c042ec273ea036957ffe1f1c1ed.png)

起動したコンテナを右クリック、 Attach Visual Studio Code をクリックして

![](https://gyazo.com/e13500b29b62f906e5c81e5677adb036.png)

フォルダーを開く を選択します。
ここで開くフォルダーは、Attachしたコンテナのフォルダになります。

![](https://gyazo.com/f671f7b0cc9ec7fdac6dd3a69586c4fc.png)

試しにルートディレクトリを指定して、OKを押すと

![](https://gyazo.com/51bc59ffc68dd5f267a5bce817ee78d0.png)

コンテナ内のフォルダが表示されます。

![](https://gyazo.com/d4a9f20a1b66e7624c481bc55ec4fd60.png)

Dockerimageの ADD requirements.txt /work_dir/ で追加された
requirements.txt も含まれているのがわかります。

![](https://gyazo.com/a4a38115f138789c92db1d1247de87ad.png)

pip install も正しく実行され、コンテナ内の環境でコードが書けるようになりました。