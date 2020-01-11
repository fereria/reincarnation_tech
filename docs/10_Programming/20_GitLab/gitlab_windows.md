---
title: Windows 環境で GitLab の CI/CD を実行する
---
# Windows 環境で GitLab の CI/CD を実行する

Docker だと Linux 環境になってしまうので、Windows 用アプリの動作ができない  
Maya などのような Windows で動くものの動作テストができないなどの問題があるので  
Runner を「Shell」にして登録する。

![](https://gyazo.com/c702ceb943c57557787c33b9315ce8bf.png)

```
gitlab-runner register
```

で、登録したときに  
Executer を **「Shell」** にして登録する。

次に、admins/Runner 画面で  
上で登録した Runner の設定画面を開き、Run untagged jobs 　のチェックを ON にしておく。

## 実行してみる

準備ができたら、簡単な JOB を投げてみる。

.gitlab-ci.yml の内容はこんな感じ。

```
stages:
  - build

build_job_test_win:
  stage: build
  script:
    - cd test_repos
    - main.py
```

![](https://gyazo.com/995d6b3cbc9c80af4e45f1636079a824.png)

プロジェクトの構成はこんな感じで、

```python
# -*- coding: utf-8 -*-
print "Hello World"
```

main.py は、プリントするだけにする。

![](https://gyazo.com/0b5816b52594b6bb2c9d46395b58a83d.png)

GitLab に Push すると、CI が実行される。

実行されると、Runner 側にクローンが作成されて  
スクリプトの内容が実行される。

Shell で Runner を指定した場合は、

![](https://gyazo.com/3064ca328c3c824efee1f7a91c4ae1a5.png)

gitlab-runner.exe が押してあるフォルダ下に「builds」が作成され  
その下に

![](https://gyazo.com/d69d7833e2351b305b5799fdd894e9cb.png)

Runners のプロジェクトで指定された ID（この場合 5fddcc20）のフォルダが  
builds 下に作成され

![](https://gyazo.com/7b74d8a2cfe8351fbaa500cc38c4c220.png)

クローンが作成される。  
このままだと、環境が隔離されないので  
Python の場合は pipenv などでクローズドな環境を毎回構築するようにしげあげると良い。
