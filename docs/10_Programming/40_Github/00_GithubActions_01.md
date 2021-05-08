---
title: GithubActionsで自動化(1) 基本構造
tags:
    - Github
    - GithubActions
    - 自動化
description: GihtubActionsの基本構文 jobs-steps
---

GithubActionsでの書き方の基本的な部分のメモ。

## 必須の構造

{{'92b388a198626ba073bdf200b06ed542'|gist}}

まず、実行したい処理（＝アクション）を定義します。
アクションは、 .github/workflows 以下に yml ファイルとして記述します。
必要なのは、 name on jobs の３つ。
nameは、このアクション自体の名前。
on は、実行トリガーの指定。
jobs は、実際に実行したい処理を記述します。

![](https://gyazo.com/b81cee1eb78e592efc35dbe28701df00.png)

![](https://gyazo.com/efde87c3511df9ed35df7463fa5c135c.png)

このサンプルの場合、 push（すべてのブランチに対して）した場合に
jobs 以下の内容が実行されます。

stepsが１つのコマンド、そのコマンドのかたまりがjobs。

実行するコマンドは、 stepsの runに書く。
idは、stepsを特定するための名前（変数名のようなもの）
依存や、別ステップから値を参照したい場合は、 names ではなく id を使用することになる。
小文字推奨。

## jobsの依存関係

{'f9fbac33cf9d46f0cf8965678e2bbe13'|gist}

jobは依存関係を作ることができる。

![](https://gyazo.com/152867a26d4a237f4eb6c79c7ab07994.png)

上の例の場合、 jobs_2 は 1の処理が完了してから実行される。
依存の作り方は、 jobs以下に needs で、 jobsID(jobs_1: この部分)を指定する。

## 環境変数

{{'11e47b080c6686eed8e18c309fb45783'|gist}}

環境変数は env: で指定できる。
この例の場合は指定Job以下で使用できる環境変数を定義しているが、
同様に アクション・ステップにも envは指定することができる。

環境変数を使うには $\{\{ env.##### \}\} を使用する。

## outputs

{{'36083938b950ae4cb6fb08c463625a3d'|gist}}

ジョブの結果の値などを、別のジョブやプロセスに渡したい場合
outputs構文を利用する。
https://docs.github.com/ja/actions/reference/workflow-commands-for-github-actions#about-workflow-commands
これはワークフローコマンドと呼ばれるもので、
:: ～ の構文で、指定の処理を実行できる。

```
::set-output name=<key>::<value>
```
outputに指定する場合は、このようにする。
こうすると、

{{'2181368ca77f7d858aa62f0a0a2af330'|gist}}

で、指定した値を別ステップから取得できる。

job間で値をやり取りしたい場合は、
job以下の

```yml
outputs:
  key: value
```

で指定すると、

{{'62944286e6b2f9224056dca7718cdf34'|gist}}

job_id指定で値を取得できる。

## if文

各ステップ・ジョブに対して、if文で実行するかを指定できる。

{{'d4f9418f1eaac928d293fcdfc129adb3'|gist}}


別のジョブの outputs次第で処理を分けるといったことができる。

![](https://gyazo.com/6f7e6c8bb6f536c5a1818c35b55ddc66.png)

この例の場合、 jobs_1 の outputs の値によって、 success か error のジョブを実行する。

### Stepの結果によって処理をかえたい

{{'fa19b1fb80245d117076746e2716e529'|gist}}

ifはステップでも使用できる。
各ステップごとの結果によって処理を切り替えるようなこともできて

![](https://gyazo.com/13f2aef088b0b98e7433e297338a664c.png)

最初のステップの結果によって、移行のステップを切り替える...といったことができる。

## 参考

* https://docs.github.com/ja/actions/reference/