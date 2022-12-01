---
title: ファイル名を入れるだけで自動でリンクを作りたい
tags:
    - macro
    - mkdocs
    - python
description:
---

表題の通りですが、mkdocs で記事を書くときに
サイト内リンクを書くとすると、相対パス or 絶対パスで記述する必要があって
ディレクトリ階層の変更がものすごくめんどくさいので
macro を書いて自動化することにしました。

```python
def getHeaderYaml(path):
    """
    mdのヘッダーに書かれているYaml形式のメタデータをDictで取得する
    """

    with codecs.open(path, "r", 'utf-8') as f:
        lines = f.readlines()

    flg = False

    retVal = []

    for i in lines:
        if flg and i.strip() == "---":
            # 最後の ---
            break
        elif not flg and i.strip() == "---":
            # 最初の ---
            flg = True
        else:
            retVal.append(i)

    if len(retVal):
        return yaml.safe_load("".join(retVal))
    return None


def searchMarkdownFile(fileName, word=""):

    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'docs')):
        for f in files:
            bn, ext = os.path.splitext(f)
            if ext == ".md" and bn == fileName:
                path = os.path.join(root, f)
                header = getHeaderYaml(path)
                buff = root.replace("\\", "/").split("/docs/")
                linkPath = f"/reincarnation_tech/{buff[-1]}/{bn}"
                linkText = word if word != "" else header['title']
                return f":fa-external-link: [{linkText}]({linkPath})"
    return ""

def define_env(env):

    @env.macro
    def markdown_link(filename, word=""):
        return searchMarkdownFile(filename, word)
```

macro用の main.py に markdown_link を追加して、ファイル名（名前だけ）とリンク用の文字列を
引数を受け取る関数を定義します。

![](https://gyazo.com/1a752123d2e4a9cac0ddef6ea9fc8d81.png)

Markdown上では、このように記述します。

{{markdown_link('99_mkdocs_sample.md')}}

その結果がこの通り。

やっていること自体は非常にシンプルで、
docs以下にある mdファイルをさがし、引数で指定した名前にマッチした markdownのファイルに
アクセスするためのリンクを生成します。

mdファイル名が重複してしまうと成立しないのですが
自分の場合名前は重複しないようにつけているのでこれで問題ありません。

この方式でリンクを書いておけば、ファイルの沖場所が変化しても
ページをビルドした時に自動的に解決してくれます。

あとは、ページのタイトル名をリンクの文字列にしてくれるので
毎回Title名を確認したりしなくて済むのもGoodです。