---
title: 続、mkdocsを設定する(自動ビルド)
---

mkdocs のバージョンをアップするついでに、色々と環境を更新したのでメモ。

## mkdocs.yml の更新

まず、MaterialTheme 関連。  
特に何も考えずバージョンアップをしたら互換性なくなっているところが  
多くなっててエラーまつり。  
というわけで、mkdocs.yml を更新するところから。

https://github.com/fereria/reincarnation_tech/blob/master/mkdocs.yml

mkdocs の元になってる md や yml は全部 GitHub にありますので、全部見たい人はそちらから。

今までとの大きな変更点は、フォルダ階層が mkdocs.yml に書いていたのが  
なくなりました。

```yaml
plugins:
    - git-revision-date-localized:
          type: iso_datetime
          locale: ja
    - search:
          lang:
              - en
              - ja
    - awesome-pages
```

nav:の定義自体はなくても平気なのですが、その場合  
フォルダ名に日本語が入ってしまうので都合が悪い...ということで  
スクリプトを使用してこのツリーを自動生成していました。

awesome-pages

このあたりの置き換わりが、awesome-pages というプラグイン。  
このプラグインをいれると、Folder 以下に .pages という yml で書かれた定義を読み込んで  
Folder 名や、Folder 以下のページの並び順を制御できるようになっています。

```
title: Documentation
```

これを利用して、並び替え制御用にいれた数字や日本語名の時間をした Folder の Title を  
定義するようにしています。

https://github.com/fereria/reincarnation_tech/blob/master/create_mkdocs_pages.py

このファイルは、もちろん手で毎度作るのはめんどくさいので  
スクリプトで Deploy 時に自動生成するようにしています。
（後述の GithubAction で実行）

md の書くページの Title 名も、今までは自前の処理で作っていましたが、
markdown の冒頭に

```
---
title: mkdocs を設定する
---
```

title を指定することで、メニューの Title にしてくれる機能ができたので  
こちらで指定するようにしました。
おかげで自動生成のフローが大幅にスッキリしました。

### pipenv 指定

構造が整理できたのでビルドする環境にも手を入れます。  
今まではなんとなく使うプラグインを素の Python3 環境に pip でインストールしていましたが  
自動ビルドするにはそれだとマズいので、pipenv での環境構築をするようにしました。

プロジェクトルートに Pipfile を作り、
使用するプラグイン類は Pipenv 経由でインストールします。

```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
mkdocs="==1.1.2"
mkdocs-awesome-pages-plugin="==2.2.1"
mkdocs-git-revision-date-localized-plugin="==0.4.8"
mkdocs-macros-plugin="==0.4.9"
mkdocs-markdownextradata-plugin="==0.1.3"
mkdocs-material="==5.3.0"
mkdocs-minify-plugin="==0.2.1"
markdown-blockdiag="==0.7.0"
fontawesome-markdown="==0.2.6"
mkdocs-material-extensions = "*"
hbfm = "*"

[requires]
python_version = "3.6"
```

Pipfile はこんな感じ。  
mkdocs は結構バージョンによって動く・動かないが起きてしまうので  
使用するバージョンは固定しておきます。

ここで指定した環境が GitHubAction での環境にもなるので  
必要なパッケージが揃っていて、ちゃんとビルドできるようにします。

Pipfile を用意さえしておｋば、 pipenv install で、指定の Python バージョンに  
指定のモジュールが入った環境が作れるので便利です。
詳しい内容は、{{markdown_link('pipenv_statup')}} にまとめてあるので、そちらを参照をば。

### Github Action で自動ビルド

![](https://gyazo.com/27f2009b05f2e59fe9359b20092f55d7.png)

ここまで準備ができたら、Github 側に自動ビルド環境を作ります。  
Github には無料で使える CI 環境があるので、ここに mkdocs をビルドする処理を書いていきます。

![](https://gyazo.com/b5107ed38526c2b5a80cbde4e60269aa.png)

まずは、ドキュメントのリポジトリルート下に .github/workflows というフォルダを作り、  
その中に yml ファイルを作ります。

```yaml
name: Python application

on:
    push:
        branches: [master]
    pull_request:
        branches: [master]

jobs:
    build:
        runs-on: ubuntu-latest

        steps:
            - name: Git config
              run: |
                  git config --global core.symlinks true
                  git config --global user.name "Megumi Ando"
                  git config --global user.email "remiria@flame-daybreak.net"

            - name: Checkout
              uses: actions/checkout@v2
              with:
                  fetch-depth: 0

            - name: Set up Python 3.6
              uses: actions/setup-python@v1
              with:
                  python-version: 3.6
            - name: Install Pipenv
              run: |
                  pip install pipenv
                  pipenv install

            - name: Mkdocs
              run: |
                  python create_mkdocs_pages.py
                  pipenv run mkdocs gh-deploy
```

そこに、実行する処理を書いていきます。

今回は、master ブランチに Push したタイミングで、mkdocs のビルドを実行するようにします。  
参考にしたのは
https://roy-n-roy.github.io/mkdocs/githubActions/
こちらのサイト。
とりあえず動くところまでなんとか書いてみました...感があるので、  
Actions に関してはもうちょっと色々調べたいところです。

![](https://gyazo.com/6df098b7405ae778f441509f8ac81654.png)

この yml を Push すると  
Actions に Workflow が追加されます。  
そして、CI が実行されると右側の Event にビルド結果が表示されます。

![](https://gyazo.com/fafe90353d47ffb15bd4f0c7c2650d53.png)

各 Event は、こんな感じでログの確認ができるようになります。

で。

1. ビルドしたいリポジトリをクローン
2. Pipenv を使用した環境構築
3. .pages の自動生成
4. Mkdocs のビルド
5. Deploy

というのが自動で実行されて  
処理が終わると、GithubPages 側に変更が反映されます。

### まとめ

そんなかんじで、今までは手元で mkdocs gh-deploy していた関係で  
アップしたくない下記途中のファイルは色々避けておくとかしないといけなかったり  
自分の手元の環境じゃないと記事が更新しにくかったりしたのですが  
Deploy 部分が Github 側での自動処理に変わったので  
どこでも Clone して記事を書いて Push すれば、記事が更新できるようになりました。

Github に元の .md をアップするのも、今までは mkdocs.yml に フォルダの階層を  
スクリプトを生成する処理を入れていたので、  
記事を書く → 手元で Deploy→Yaml を Push みたいな変則的な手順を取る必要がありましたが  
それもなくなりました。

GithubActions も、調べてみたら結構かんたんにいろんな自動処理がかけることがわかったので  
このあたりも別途検証していきたいです。
