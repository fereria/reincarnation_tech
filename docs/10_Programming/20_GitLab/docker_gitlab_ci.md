---
title: Docker で Runner を使用する\_セットアップ編
---
# Docker で Runner を使用する\_セットアップ編

まず、Windows の PC に、Docker をインストールする。

![](https://gyazo.com/9542ce3548d18892f7cc393f0f276e10.png)

インストールしたのに、何故かエラーになって起動できなかったのですが  
原因は、BIOS 側の Intel-VT が ON になっていないせいだった。

次に、GitLab-Runner をインストールする。

https://docs.gitlab.com/runner/install/windows.html

手順は公式参考にして、 gitlab-runner の 64bit 用 exe をダウンロードして、

```
C:\GitLab-Runner
```

このフォルダにコピーする。  
次に、管理者モードのコマンドプロンプトを開き、上のフォルダに移動後

```
gitlab-runner install
gitlab-runner start
```

![](https://gyazo.com/2b77af47149d63c1960cabdafc68445c.png)

GitLabRunner をサービスに登録する。  
サービス登録が終わったら、GitLab への登録をする。

GitLab のプロジェクト →Settings→CI/CD を開き、Runners Settings を開く。

![](https://gyazo.com/67e413b0a1f7938d1100515561c46a83.png)

Setup a specific Runner manually ないにある URL と Token を確認しつつ、
コマンドプロンプトに、

```
gitlab-runner register
```

![](https://gyazo.com/bc932ba1d7252a7df04fb08d63cced8d.png)

と入力し、GitLab の URL→Token→ 登録名 →Tag 　を入力する。  
入力すると、どのモードで実行するかを聞かれるので「docker」を選択する。

![](https://gyazo.com/d3c498aeb73210cbaba80c7f26223600.png)

登録が完了すると、GitLab 側に Runner が登録される。  
Project 側で Runner を登録すると、その Runner はプロジェクト専用になる。  
SharedRunner に登録すると、複数プロジェクトでの共通になるらしいが  
現状そちらへの登録だとうまく動かなかった。

Runner を登録したら、GitLab 側伸した準備は完了。

## .gitlab-ci.yml を作成する

準備ができたら、CI を走らせるための設定ファイルを作成する。  
Git のプロジェクトルートに、 **.gitlab-ci.yml** ファイルを作成して  
とりあえずコミットしてみる。

```
image: python:2.7

stages:
  - build

before_script:
  - pip install --upgrade pip

build_job1:
  stage: build
  script:
    - pip install sphinx
    - ls
```

中身はとりあえずシンプルにこんな感じにする。  
基本は

```
<name>:
 - コマンドプロンプトで実行するコマンド
```

のような構造になっている。  
その中で、いくつか特殊ないみを持つものがある。

image 　が、Docker のコンテナ名で  
こんかいは Python2.7 でテストするのでその名前にしている。

before_script が、メインの処理が始まる前に実行する内容。

stages は、実際に実行する処理内容。

```
<name>:
  stage:<stage_name>
  script:
    - command1
    - command2
```

メインの処理内容は、こんな形が基本になっていて  
ここの stage で書いた内容を stage:に記載する。

.gitlab-ci.yml を、Git にコミットするとジョブが実行される。

![](https://gyazo.com/35e55f1d83e999824e9b3831c48d1d56.png)

プロジェクトの CI/CD の Jobs を見ると、

![](https://gyazo.com/73bb6792d1d63079851f917b56395200.png)

JOB が追加される。

![](https://gyazo.com/c7a483e2ecf67f37bbe125a1adf67380.png)

正しく Runner が登録されていると、JOB が開始されて、  
Docker で、image で指定したコンテナが作成されて  
stage で登録した JOB が実行される。  
Docker で毎回環境が構築されるので、JOB のスクリプトなどで pip install XXXX を使用して  
使用しているパッケージをいれるなどをしてあげる。

## Shell 時に Job が走らない場合の対処法

Windows 環境で CI を動かしたい場合は docker ではなく shell を使用するが、  
ステータスはグリーンになっているにもかかわらず JOB がスタックしてしまい  
処理が始まらない現象が発生した。

![](https://gyazo.com/f69eb02c5f0a6253d88198ec7aa61fed.png)

原因は、JOB にタグがない場合は走らないのチェックが Off の場合  
Shell の処理が開始しないせいだった。  
（Docker の場合は、OFF でも JOB が走った）

Jenkins とは違い、yml 形式で実行内容を記載しないと行けない都合  
若干敷居が高いきがするけれども、  
テキストファイルでコマンドなどを準備できるので、  
慣れてしまえばこちらの方が扱いやすい気がする。  
Maya 等を自動で動かしたい場合は、Docker ではなく Shell にする感じ？  
など、このあたりはまだ未検証だけれども  
色々と使えそう。

## 参考

- https://qiita.com/yurano/items/a7804d987ccff37b1a9d
