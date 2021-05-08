---
title: GithubActionsで自動化(2) リリース
tags:
    - Github
    - GithubActions
    - 自動化
description: GithubActionsでコードをリリースする
---

## Githubのリリースとは

基本は [前回](00_GithubActions_01.md)まとめたので、今回はビルド結果をリリースする方法について。

![](https://gyazo.com/69c35b9f5cba3fb76706fb762877349f.png)

Githubには、リポジトリのコードをビルドした結果を「Release」という形で
配布用に公開することができる。

![](https://gyazo.com/bba50b92bdb214d85c88dce1d8a1bdff.png)

リリースは、タグ単位で作成することができて、

![](https://gyazo.com/b893b2c04628bfd428f7c7ac12872c29.png)

タグページの Draft a new release から、

![](https://gyazo.com/33c4b6990f4c820956ca16a1a92563e5.png)

タグを指定して、作成できる。

![](https://gyazo.com/81a0b53a3061358c61ecb51ff9a903fd.png)

作成すると、タグを指定した段階のリポジトリのソースコードと
GithubActionsを使用してビルドした結果などを
ダウンロードできるようにできる。

## 自動化

{{'1c6dea48e6ccfee3a83a2c34a69cac2b'|gist}}

スクリプトを実行した結果を、ダウンロードできるようにしたサンプル。

### タグの追加でアクション実行

すべてのPushに対してリリースが作られれてしまうと色々まずいので
指定のバージョンのみビルドするようにしたい。
そういう場合は、タグを使う。

タグは、コミット単位で指定することができる。
コードをコミット・プッシュした段階で、
```
git tag <tagname>
```
でタグを作成。
作成すると、最後のコミットに対してタグが追加できる。

この段階だと、ローカルのリポジトリに反映されただけなので

```
git push origin <tagname>
```

で、Github側にタグを反映できる。

```
on:
  push:
    tags:
      - "release-v*"
```

アクション側のトリガーに、 tagをプッシュした場合のみに変更。
さらに、タグ名も release-v1.0.0v のようにリリースタグがついたとき
のみに実行するようにする。

### Actionsの便利なジョブを使う

GithubActionsには、自分でジョブを書くだけではなく
公開されたジョブのプリセットのようなものを「使う」事ができる。
```
      - name: Checkout
        uses: actions/checkout@v2
        with:
          fetch-depth: 0
```
たとえば、Gitのリポジトリをクローンしてくるような処理。
使いたい場合は、 run ではなく uses を使い
ユーザー名/リポジトリ名@ブランチ のように、指定する。

https://github.com/actions

公式で用意されているのはここにある。

```
      - uses: satackey/action-docker-layer-caching@v0.0.11
        continue-on-error: true
      - name: Docker Compose
        run: docker-compose -f docker/docker-compose.yml up --build -d
```

チェックアウト以外に、Dockerのイメージビルドをキャッシュして
変更がなければ高速化できる action-docker-layer-caching のように、だれかが公開してくれている
アクションも使うことができる。

大抵のものは調べたら出てくるので、これを利用して処理を自動化すると良い。

## Artifactの追加

Artifactとは、アクション実行時の生成物を保存しておくことができる機能。

```yml
      - uses: actions/upload-artifact@master
        with:
          name: export usda
          path: ./src/usd/HelloWorld.usda
```

例えば、スクリプトを実行したときにできたファイルを、指定すると、

![](https://gyazo.com/d6ee14e3906249d3a51927bdee32b1cc.png)

Actionsのページからダウンロードできるようになる。

## タグ名を取得する

リリースでダウンロードできるようにするzipに、Gitのタグを使いたい場合。

```
      - name: Get the version
        id: get_version
        run: echo ::set-output name=VERSION::$(echo $GITHUB_REF | cut -d / -f 3)
```

事前のステップで、outputsにセットするようにすればよい。
タグ名は github.ref を使用すれば取得できるが、そのままだと refs/tag/tagname になってしまう。
なので、 cut を使用して3つ目のタグ部分だけを切り出して、 outputにセットする。

{{'69037949e08d487718aefdeebe7c8b4f'|gist}}

outputにセットされていれば、その値は steps.get_version.outputs.VERSION で取得できるので
これを zip 作成時に使う。

## リリース

最後に、生成物をリリースする。

{{'5cf9b12fa0444c14ea656330b7b9c769'|gist}}

リリース部分もすでに便利なアクションが用意されているのでそれを使用する。

upload-release-asset の asset_path で、リリースをするファイルを指定できるので、
事前に作っておいたzipを指定する。

with: は、用意されたアクションに対して渡す引数のようなものなので
必要な情報を with 以下 key: value で指定すればOK。

## まとめ

このアクションを作っておけば、指定タグをPushしたタイミングで自動でビルドが走り
その成果物が自動でリリースされる。

注意点として、このリリース処理はタグがついていることが前提になっていて
トリガーを tags ではなく通常のpushにして
タグがついていない状態で実行されると、 ref/heads/master というタグが自動で生成されて
ブランチ名と同様のタグができてしまい、プッシュしようとするとエラーになっていた。
（ものすごいハマる）

その時はGithubのTagから ref/heads/master を削除して、
アクションのトリガーは tag 指定のときのみに限定する。