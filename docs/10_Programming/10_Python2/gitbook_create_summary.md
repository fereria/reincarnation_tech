---
title: GitBook の SUMMARY ファイルを自動作成
---
# GitBook の SUMMARY ファイルを自動作成


GitBook のサマリーファイルを作成するのが面倒なのと  
自分のスタイルに合ったものが見つからなかったので  
Python を使用して作成しました。

Gitbook の公式サイトにアップした場合は、フォルダや Markdown ファイルに  
日本語が入っていてもいい感じにアルファベットに置き換えてくれるのですが  
その場合、パスがわけわからない感じになってしまう上に  
GitBook サイト以外でビルド → 公開しようとすると  
パスが通らなくなってしまってよろしくない。

なので、自分で作成した SUMMARY 作成スクリプトでは、

SUMMARY に記述する名前を

```
<!-- SUMMARY:メニューに表示される名前 -->
```

このように markdown 内にコメントとして記載し、

![](https://gyazo.com/6a4c42f0fe28e9ab7cb4dffe82dde7f4.png)

ファイル名はアルファベットを使用したファイル名にするようにしました。  
フォルダ名に関しては、スクリプト内で置換する文字を指定して  
置きかえをするようにしました。

メニュー内の並び順はファイル名になっているので  
10\_#####  
このように数字をいれるようにしたいのですが  
メニューに数字入れるのはあまり好きではないので  
SUMMARY に書き出すときには数字部分は削除するようにしています。

実際にフォルダの中を検索してくる部分は再帰処理を使用しています。  
(walk だと意図しない順序になってしまうので却下)

root 移行のフォルダ階層の数によってインデントを変更するようにして  
終わりまで処理しています。

あとは、このスクリプトを VSCode のビルドタスクにセットして  
GitHub にコミットする前に実行するようにしました。

## 参考

- https://qiita.com/hasepy/items/8e6a0757da1ce074ce87

## コード

```python
#!python2
# -*- coding: utf-8 -*-
"""
GitbookのSUMMARY.mdを自動で作成する。
"""

import codecs
import re
import os.path
import glob

# --------------------------------------------------------- #
# 設定
# --------------------------------------------------------- #

GITBOOK_ROOT = u"<root_path>"
GITBOOK_DOCS = u"<docs_path>"

# 日本語のIndexにしたいものは、フォルダ名から↓の名前に置換する
FOLDER_REPLACE_STRING = {
    "basic_operation": u"基本操作",
    "data_structure": u"データ構造",
    "terms": u"用語"
}

# --------------------------------------------------------- #

EXCLUSION = [".git", ".vscode", ".history", "_book", "node_modules"]


def create_summary(summary_path, root_path, indent_space="  "):
    """
    root_path以下にあるフォルダ階層/mdファイルでSUMMARY.mdを作成する
    """

    write_val = []

    def recursive_file_check(path):
        if os.path.isdir(path):
            if root_path != path:
                gb_path = path.replace("\\", "/").replace(root_path + "/", "")
                if has_markdown(path):
                    buff    = gb_path.split("/")
                    indent  = (len(buff) - 1) * indent_space
                    write_val.append(indent + "- " + replace_title_folder_name(re.sub("^[0-9][0-9]_", "", buff[-1])))
            files = os.listdir(path)
            for file in files:
                recursive_file_check(path + "/" + file)

        else:
            # SUMMARYに記載するMarkdownまでのパス
            bn = os.path.splitext(os.path.basename(path))[0]
            if bn != "SUMMARY":
                relative_path = "docs" + path.replace("\\", "/").replace(root_path, "")
                buff = relative_path.split('/')
                summary_keyword = get_summary_word(path)
                if summary_keyword == "":
                    summary_keyword = bn
                write_val.append((len(buff) - 2) * indent_space + u"- [{0}]({1})".format(summary_keyword, relative_path))

    recursive_file_check(root_path)

    with codecs.open(os.path.join(summary_path, "SUMMARY.md"), "w", "utf-8") as f:
        f.write("\n".join(write_val))


def get_summary_word(path):
    """
    引数のPathのMarkdownファイルにあるサマリー用の名前を取得する
    """

    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()

    # サマリーのタイトル名の行を取得する
    for i in lines:
        if re.search('<!--.*SUMMARY:.*-->', i) is not None:
            buff = i
            for j in ["<!--", "-->", " "]:
                buff = buff.replace(j, "")
            buff = buff.split(":")
            return buff[1].strip()
    return ""


def replace_title_folder_name(name):

    buff = name
    for key in FOLDER_REPLACE_STRING.keys():
        buff = buff.replace(key, FOLDER_REPLACE_STRING[key])
    return buff


def has_markdown(path):
    """
    指定フォルダ以下にMarkdownファイルが存在する場合Trueを返す
    """
    buff = glob.glob(path + u"/*.md")
    if len(buff) == 0:
        if len(os.listdir(path)) == 0:
            return False
    return True


def is_exclusion_path(path):
    # 除外ファイルの場合Trueを返す
    for i in EXCLUSION:
        if re.search("/" + i, path) is not None:
            return True
    return False


if __name__ == "__main__":
    create_summary(GITBOOK_ROOT,
                   GITBOOK_DOCS)

```
