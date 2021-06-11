---
title: mkdocsでdrawioを使う
---

drawIOとは、ウェブブラウザやVSCode、
デスクトップアプリとして動作するフリーの作図ツールです。

![](https://gyazo.com/cadf06cff6d716b9f0cdf36b14b7eb23.png)

このDrawの良いところは、 ~~~.drawio という拡張子にすることで
VSCode上でも作図をすることができます。
これを利用すると、かんたんに作図をすることができます。

## mkdocs-drawio_exporter

https://pypi.org/project/mkdocs-drawio-exporter

そして、更に便利なことに、mkdocsには drawio ファイルをそのまま
画像として保存することなく貼り付けることができます。

```
![](sample.drawio)
```

このように、画像のパスを指定する部分に
貼り付けたい drawioのパスを指定すると

![](sample.drawio)

drawioの作図した結果の画像を貼り付けることができます。

### 準備

https://github.com/jgraph/drawio-desktop/releases

まず、Windowsの場合は、darwio-desktop の windows-installer を実行してインストールします。
あとは、mkdocsのプラグインを pipでインストールします。
```
pip install mkdocs-drawio-exporter
```
Windowsの場合の準備は以上です。

### Docker対応
が、、、今は、mkdocsのビルドはGithubAction上でDockerコンテナベースで実行しているので
Docker上でも動くようにしなければいけません。
Dockerの場合は、Dockerfileに以下を追加します。

```
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
```

drawio本体は dpkgでインストールできたのですが、それだけだとエラーになってしまい
docker環境上でdrawioが実行できませんでした。
https://github.com/jgraph/drawio-desktop/issues/127
解決方法は、ここに書いてあって
xvfbで仮想ディスプレイを作り、その設定が必要とのことでした。

### requirements.txt 更新

```
mkdocs-drawio-exporter
```

Docker環境のPythonにもmkdocsPluginを入れるために
mkdocs-drawio-exporter を requirements.txt に追加します。


### mkdocs.yml 設定

drawioのインストールができたら、mkdocs.ymlを変更します。

```mkdocs.yml
plugins:
  - drawio-exporter:
      cache_dir: "drawio-exporter"
      drawio_executable: null
      drawio_args: ["--no-sandbox"]
      format: svg
      embed_format: "{img_open}{img_src}{img_close}"
      sources: "*.drawio"
```
mkdocs.ymlのplugins以下に、 drawio-exporterを追加します。
注意点は、 drawio_args に --no-sandbox を追加することです。
（これを入れないとエラーになる）

https://github.com/fereria/reincarnation_tech/tree/master/docker
Dockerの環境はこちら。



## まとめ

この方法でdrawioを使用した場合、mkdocs serve でプレビューすると
drawioファイルを更新すればページ側も更新されるようになります。
すごく便利。

Docker環境上で drawio-desktopを使用する方法がかなり難しくて
用意されたdarwioのDockerをベースにしようとすると
Pythonが3.5までしか使えず。
この環境にソースコードからPython3.7をインストールしようとするとエラーになり
PythonベースでDockerfileを構築しても
snapdを使用したやり方 https://snapcraft.io/install/drawio/ubuntu だと
エラーになってインストールできず（Dockerに対応していないらしい）
dpkgでインストールしようとしてもインストールに苦戦
インストールできたとおもっても実行できずない...で、数日調べ漁る羽目になりました。

苦戦はしましたが、無事markdownをGithubにPushしたら
作図が反映されるようになったので、ページの更新がかなり楽になりそうです。